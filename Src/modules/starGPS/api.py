import cgi
import json
import logging

import geolocate as geo

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
    return ret

#  {"name": "Wolf Point", "type": "Shelter", "coords": {"x":276.443536,"y":-9.384236,"z":103.100625}}
def get_location(name):
    ret = {
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
    }
    return ret

def get_poi(name):
    pass

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

    res = get_system(data['system'])
    return '{"data":'+res+'}'


@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/location")
def getLocationInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'
    print 
    print query
    print
    data = json.loads(query)

    res = get_location(data['location'])
    return '{"data":'+res+'}'


@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/poi")
def getPOIInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    data = json.loads(query)

    res = get_poi(data['poi'])
    return '{"data":'+res+'}'

