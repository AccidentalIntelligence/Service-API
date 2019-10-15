import cgi
import json
import logging

import geolocate as geo

import db as db

from ..api_helper import *

has_config = False

# check config can be loaded
try:
    from config import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the StarCitizen API. The API will not function.")

def get_system(name):
    # return system info plus list of locations
    ret = {
        "id": 1,
        "name": "Stanton",
        "affiliation": "UEE",
        "description": "It's cool bro!",
        "locations": [
            "ArcCorp",
            "MicroTech",
            "Hurston",
            "Crusader",
            "Daymar",
            "Yela"
        ]
    }
    ret = db.get_system(name)
    return ret

#  {"name": "Wolf Point", "type": "Shelter", "coords": {"x":276.443536,"y":-9.384236,"z":103.100625}}
def get_location(name):
    test_data = {
        "Daymar": {
            "id": 2,
            "name": "Daymar",
            "designation": "Stanton IIc",
            "description": "Dusty Moon",
            "type": "Sattelite",
            "subtype": "Moon",
            "parent": "Crusader",
            "habitable": 0,
            "msl": 295.5,
            "atmo": 29.5,
            "om_radius": 464.9,
            "sattelites": [],
            "POIs": [
                {
                    "id": 3,
                    "system": "Stanton",
                    "location": "Daymar",
                    "name": "Wolf Point",
                    "owner": "Unknown",
                    "type": "Mining",
                    "altitude": 0,
                    "coords": {"x":276.443536,"y":-9.384236,"z":103.100625},
                    "facilities": "",
                }
            ]
        },
        "Yela": {
            "id": 2,
            "name": "Yela",
            "designation": "Stanton IIa",
            "description": "Cold Moon",
            "type": "Sattelite",
            "subtype": "Moon",
            "parent": "Crusader",
            "habitable": 0,
            "msl": 295.5,
            "atmo": 29.5,
            "om_radius": 464.9,
            "sattelites": [],
            "POIs": [
            ]
        },
    }
    ret = db.get_location(name)


    #ret = test_data[name]
    return ret

def add_location(data):
    # Validate data has all the proper fields and field types here...
    db.add_location(data)

    return {"result":"Success!"}

def get_poi(name, location):
    return db.get_poi(name, location)

def add_poi(data):
    # Validate data has all the proper fields and field types here...
    db.add_poi(data)

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/locate")
def getGPSLocation(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = geo.compute(data)

    return '{"data":'+res+'}'


@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/system")
def getSystemInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = get_system(data['query'])
    return '{"data":'+json.dumps(res)+'}'


#@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@set_headers({'Content-Type':'application/json'})
@register_api("stargps/location")
def getLocationInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = get_location(data['query'])

    return '{"data":'+json.dumps(res)+'}'

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/addLocation")
def addLocationInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = add_location(data)

    return '{"data":'+json.dumps(res)+'}'


#@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
#@register_api("stargps/poi")
def getPOIInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = get_poi(data['name'], data['location'])
    return '{"data":'+json.dumps(res)+'}'

