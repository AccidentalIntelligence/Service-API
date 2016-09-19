import cgi
import json
import logging
import MySQLdb
import random
import time

from ..api_helper import *

print "has_config: " + str(has_config)

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the Twitch API. The API will not function.")

import connectors.twitch as connector

def storeStatus(data, when):
    logging.debug("Storing Data: " + str(data) + " checked: " + str(when))
    db = MySQLdb.connect(host=config.dbhost, user=config.dbuser, passwd=config.dbpass, db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)

    query = """REPLACE INTO channel_status (
            channel,
            live,
            viewers,
            game,
            last_checked
        ) VALUES (%s, %s, %s, %s, %s)
        """
    params = (data['channel'], data['live'], data['viewers'], data['game'], when)

    logging.debug(query)
    logging.debug(params)

    c.execute(query, params)
    db.commit()
    db.close()

def getStreamStatus(channel):
    db = MySQLdb.connect(host=config.dbhost, user=config.dbuser, passwd=config.dbpass, db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM channel_status WHERE channel=%s", (channel,))
    res = c.fetchall()

    now = time.time()
    result = {}

    if len(res) == 0 or now - res[0]['last_checked'] > 60:
        logging.debug("Channel not listed, or timed out. Getting status from Twitch API")
        result = connector.getStreamStatus(channel)
        if result:
            storeStatus(result, now)
        else:
            result = {'error':'Failed getting status from Twitch API'}
    else:
        logging.debug("Channel found in DB, retrieving")
        result = res[0]

    return result

def getStreamCount(game):
    result = {}
    result['count'] = connector.getStreamCount(game)
    return result

def getRandomStream(game):
    count = connector.getStreamCount(game)
    offset = random.randrange(count-100)
    result = connector.getStreamAtOffset(game, offset)
    return result


def getValues(dic, keys):
    ret = {}
    for key in keys:
        ret['key'] = dic['key']
    return ret

####[ API Functions ]###########################################################

@register_api("twitch")
def getTwitchResponse(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for Twitch API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return '{"error":"missing user token"}'
    if not 'a' in qs:
        return '{"error":"missing action type"}'
    data_req = qs['a'][0]

    # status request of a given channel
    if data_req == 'status':
        logging.info("Action requested: status")
        if not 'q' in qs:
            return '{"error":"missing query string"}'
        query = qs['q'][0]
        result = getStreamStatus(query)
        return json.dumps(result)

    # count of all live streams
    elif data_req == 'count':
        logging.info("Action requested: count")
        if 'g' in qs:
            game = qs['g'][0]
        else:
            game = ""
        result = getStreamCount(game)
        return json.dumps(result)

    # returns a random streams
    elif data_req == 'random':
        logging.info("Action requested: random")
        if 'g' in qs:
            game = qs['g'][0]
        else:
            game = ""
        result = getRandomStream(game)
        return json.dumps(result)
