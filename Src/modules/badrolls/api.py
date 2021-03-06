import cgi
import json
import logging
import MySQLdb
import random
import time

from ..api_helper import *

has_config = False

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the badrolls API. The API will not function.")


def getInfo(name):
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname, use_unicode=True, charset="utf8")
    sql = "SELECT * FROM characters WHERE name=%(name)s"
    c = db.cursor(MySQLdb.cursors.DictCursor)
    params = {
        "name":name
    }
    c.execute(sql, params)
    res = c.fetchall()[0]
    db.close()
    return res

def getName(name):
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname, use_unicode=True, charset="utf8")
    sql = "SELECT name FROM characters WHERE twitch=%(twitch)s"
    c = db.cursor(MySQLdb.cursors.DictCursor)
    params = {
        "twitch":name
    }
    c.execute(sql, params)
    res = c.fetchall()[0]
    db.close()
    return res

def updateChar(data):
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname, use_unicode=True, charset="utf8")
    sql = """UPDATE characters
                SET ac=%(ac)s,
                    dex=%(dex)s,
                    dex_prof=%(dex_prof)s,
                    intel=%(intel)s,
                    int_prof=%(int_prof)s,
                    cha=%(cha)s,
                    cha_prof=%(cha_prof)s,
                    wis=%(wis)s,
                    wis_prof=%(wis_prof)s,
                    str=%(str)s,
                    str_prof=%(str_prof)s,
                    class=%(class)s,
                    full_name=%(full_name)s
                    WHERE name=%(name)s"""

    c = db.cursor(MySQLdb.cursors.DictCursor)

    c.execute(sql, data)
    db.commit()
    db.close()
    return {"success":"true"}


####[ API Functions ]###########################################################

#@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
#@register_api("badrolls")
def getResponse(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return '{"error":"missing user token"}'
    if not 'a' in qs:
        return '{"error":"missing action type"}'
    action = qs['a'][0]

    if action == "info":
        logging.info("Action requested: info")
        if not 'char' in qs:
            return '{"error":"Missing character name. Specify with: char=<name>"}'
        query = qs['char'][0]
        result = getInfo(query)
        return json.dumps(result)

    if action == "name":
        logging.info("Action requested: name")
        if not 'twitch' in qs:
            return '{"error":"Missing twitch id. Specify with: twitch=<id>"}'
        query = qs['twitch'][0]
        result = getName(query)
        return json.dumps(result)

    if action == "update":
        logging.info("Action requested: update")
        if not 'data' in qs:
            return '{"error":"Missing character data. Specify with: data={...}"}'
        data = json.loads(qs['data'][0])
        result = updateChar(data)
        return json.dumps(result)
