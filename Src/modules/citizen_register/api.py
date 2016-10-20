import cgi
import json
import logging
import MySQLdb
import random
import time
import urllib2
import urllib

from ..api_helper import *

'''

https://robertsspaceindustries.com/api/starmap/bootup

data.species
data.systems.rowcount
data.systems.resultset[]
    .code
    .name
    .type
    .id
    .description

https://robertsspaceindustries.com/api/starmap/bookmarks/find
https://robertsspaceindustries.com/api/starmap/celestial-objects/SOL

data.resultset[].celestial_objects[]
    .type (PLANET)
    .affiliation
        .id
        .name
        .code
    .code
    .descirption
    .designation
    .habitable
    .id
    .name
    .subtype.name
    .sensor_danger
    .sensor_economy
    .sensor_population
    .thumbnail.source

https://robertsspaceindustries.com/api/starmap/celestial-objects/SOL.PLANETS.EARTH

.data.resultset[].children[]
    .type (LZ, SATELLITE)
    .code
    .description
    .designation
    .id


'''

def getSystems():
    url = "https://robertsspaceindustries.com/api/starmap/bootup"
    try:
        db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)

        # First - check to see if we already have data for the search term
        c = db.cursor(MySQLdb.cursors.DictCursor)

        res = urllib2.urlopen(url,"")
        data = json.load(res)["data"]
        systems = []
        for system in data['systems']['resultset']:
            sql = "INSERT INTO systems (code, name, description, type, id) VALUES (%s, %s, %s, %s, %s)"

            systems.append(system['code'])
            sysdata = (
                system['code'],
                system['name'],
                system['description'],
                system['type'],
                system['id']
            )
            #c.execute(sql, sysdata)
        print "Systems Added: " + ", ".join(systems)

    except:
        pass

def getPlanets():
    pass

def getCities():
    pass

getSystems()

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'http://capnflint.com'})
@register_api("registry")
def getResponse(query):
    pass
