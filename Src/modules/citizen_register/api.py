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

def storeSystem():
    db = MySQLdb.connect(host='localhost',user='reguser',passwd='Citiz3n5h1p',db='citizen_register')

    # First - check to see if we already have data for the search term
    c = db.cursor(MySQLdb.cursors.DictCursor)

def getSystems():
    url = "https://robertsspaceindustries.com/api/starmap/bootup"
    try:


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
        print "oops!"
    return systems

def getPlanets(system):
    url = "https://robertsspaceindustries.com/api/starmap/star-systems/" + system
    print url
    try:
        res = urllib2.urlopen(url, "")
        data = json.load(res)["data"]
        planets = []
        for obj in data['resultset'][0]['celestial_objects']:
            if obj['type'] == "PLANET":
                sql = "INSERT INTO planets (code, name, descirption, type, designation, habitable, danger, economy, population, thumbnail, affiliation, system) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                planets.append(planet['code'])
                if planet['habitable']:
                    planet['habitable'] = 1
                else:
                    planet['habitable'] = 0
                if thumbnail in planet.keys():
                    planet['thumbnail'] = planet['thumbnail']['source']
                else:
                    planet['thumbnail'] = ""
                try:
                    planet['danger'] = int(planet['danger'])
                    planet['economy'] = int(planet['economy'])
                    planet['population'] = int(planet['population'])
                except:
                    print "Failed conversion..."
                    planet['danger'] = planet['economy'] = planet['population'] = 0

                planetData = (
                    planet['code'],
                    planet['name'],
                    planet['description'],
                    planet['subtype']['name'],
                    planet['designation'],
                    planet['habitable'],
                    planet['danger'],
                    planet['economy'],
                    planet['population'],
                    planet['thumbnail'],
                    int(planet['affiliation'][0][id]),
                    system
                )
                #c.execute(sql, planetData)
        print "Planets added: " + ", ".join(planets)
    except:
        print "oops!"
    return planets

def getCities(planet):
    pass

systems = getSystems()
planets = []
cities = []
for system in systems:
    planets.append(getPlanets(system))
    for planet in planets:
        cities = getCities(planet)

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'http://capnflint.com'})
@register_api("registry")
def getResponse(query):
    pass
