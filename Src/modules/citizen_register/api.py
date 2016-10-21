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

def storeSystem(sysData):
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)
    sql = "INSERT INTO systems (code, name, description, type, id) VALUES (%s, %s, %s, %s, %s)"

def storePlanet(planetData):
    sql = "INSERT INTO planets (code, name, description, type, designation, habitable, danger, economy, population, thumbnail, affiliation, system) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    c = db.cursor(MySQLdb.cursors.DictCursor)

def storeCity(cityData):
    sql = "INSERT INTO homes (code, name, description, planet, system) VALUES (%s, %s, %s, %s, %s)"


def updateDatastore()
    systems = starmap.getSystems()
    planets = []
    cities = []
    for system in systems:
        newPlanets = starmap.getPlanets(system)
        for planet in newPlanets:
            cities = cities + starmap.getCities(planet, system)
        planets = planets + newPlanets
    result = {
        'success': 1,
        'systems': len(systems),
        'planets': len(planets),
        'cities': len(cities)
    }
    logging.info("Total Systems: " + str(len(systems)))
    logging.info("Total Planets: " + str(len(planets)))
    logging.info("Total Cities: " + str(len(cities)))

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'http://capnflint.com'})
@register_api("registry")
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
