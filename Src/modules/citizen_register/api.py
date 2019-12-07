import json
import logging
import MySQLdb
import random
import time
import cgi

from ..api_helper import *

has_config = False

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the Twitch API. The API will not function.")

import connectors.starmap as starmap

def storeSystem(sysData, db):
    sql = "INSERT INTO systems (code, name, affiliation, description, type, id) VALUES (%s, %s, %s, %s, %s, %s)"
    c = db.cursor(MySQLdb.cursors.DictCursor)

    c.execute(sql, sysData)
    db.commit()

def storePlanet(planetData, db):
    logging.debug("Storing planet: " + planetData[0])
    sql = "INSERT INTO location (code, name, description, type, designation, habitable, danger, economy, population, thumbnail, affiliation, system) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    c = db.cursor(MySQLdb.cursors.DictCursor)

    c.execute(sql, planetData)
    db.commit()

def storeCity(cityData, db):
    sql = "INSERT INTO homes (code, name, description, planet, system) VALUES (%s, %s, %s, %s, %s)"
    c = db.cursor(MySQLdb.cursors.DictCursor)

    c.execute(sql, cityData)
    db.commit()

def clearData(db):
    pass

def updateDatastore():
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname, use_unicode=True, charset="utf8")
    systems = starmap.getSystems()
    planets = {}
    cities = {}
    for system in systems.keys():
        storeSystem(systems[system], db)
        newPlanets = starmap.getPlanets(system)
        for planet in newPlanets.keys():
            storePlanet(newPlanets[planet], db)
            newCities = starmap.getCities(planet, system)
            for city in newCities.keys():
                storeCity(newCities[city], db)
            cities.update(starmap.getCities(planet, system))
        planets.update(newPlanets)
    result = {
        'success': 1,
        'systems': len(systems),
        'planets': len(planets),
        'cities': len(cities)
    }
    db.close()
    logging.info("Total Systems: " + str(len(systems.keys())))
    logging.info("Total Planets: " + str(len(planets.keys())))
    logging.info("Total Cities: " + str(len(cities.keys())))
    return result

####[ API Functions ]###########################################################

#@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
#@register_api("registry")
def getResponse(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for register API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return '{"error":"missing user token"}'
    if not 'a' in qs:
        return '{"error":"missing action type"}'
    data_req = qs['a'][0]

    if data_req == 'update':
        logging.info("Action requested: update")
        return json.dumps(updateDatastore())
    else:
        return '{"error":"Unknown action"}'
