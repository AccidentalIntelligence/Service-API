import cgi
import json
import logging

import geolocate as geo

from ..api_helper import *

has_config = False

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the StarCitizen API. The API will not function.")

def get_location():
    pass

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.capnflint.com'})
@register_api("stargps/locate")
def getGPSLocation(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarGPS API"}'

    #if query == "":
    #    return '{"error":"Empty query"}'
    #qs = cgi.parse_qs(query)
    #if not 'key' in qs:
    #    return '{"error":"missing API token"}'

    #api_key = qs['key'][0]
    #if not auth_request(api_key):
    #    return '{"error":"API Key Invalid"}'

    #if not 'data' in qs:
    #    return '{"error":"Missing query data"}'

    #data = json.loads(qs['data'][0])

    data = json.loads(query)

    res = geo.compute(data)

    return '{"data":"'+res+'"}'


    
