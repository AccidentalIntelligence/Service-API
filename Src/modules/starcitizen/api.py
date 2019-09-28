import cgi
import json
import logging

from ..api_helper import *

has_config = False

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the StarCitizen API. The API will not function.")

import connectors.rsi as rsi

def getOrgInfo(sid):
    # Just pass it through for now. We can buffer this later...
    return rsi.getOrgInfo(sid)

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'https://www.sfco.info'})
@register_api("starcitizen")
def getSCResponse(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarCitizen API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return '{"error":"missing user token"}'
    if not 'a' in qs:
        return '{"error":"missing action type"}'
    data_req = qs['a'][0]

    # status request of a given channel
    if data_req == 'org':
        logging.info("Action requested: org")
        if not 'q' in qs:
            return '{"error":"missing query string"}'
        query = qs['q'][0]
        result = getOrgInfo(query)
        return json.dumps(result)

