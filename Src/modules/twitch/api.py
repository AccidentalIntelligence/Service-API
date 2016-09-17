import cgi
import json
import logging
import MySQLdb
import time

import config

import connectors.twitch as connector

def storeStatus(data, when):
    logging.debug("Storing Data: " + str(data) + " checked: " + str(when))
    db = MySQLdb.connect(host=config.dbhost, user=config.dbuser, passwd=config.dbpass, db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)

    query = """INSERT INTO channel_status (
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
            result = "{'error':'Failed getting status from Twitch API'}"
    else:
        logging.debug("Channel found in DB, retrieving")
        result = res[0]

    return result




def getTwitchResponse(query):
    if query == "":
        return "{'error':'empty query'}"
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return "{'error':'missing user token'}"
    if not 'c' in qs:
        return "{'error':'missing query string'}"
    result = getStreamStatus(qs['c'][0])
    return JSON.dumps(result)
