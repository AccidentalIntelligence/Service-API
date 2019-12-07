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

def _getOrgInfo(sid):
    # Just pass it through for now. We can buffer this later...
    return rsi.getOrgInfo(sid)

####[ API Functions ]###########################################################

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'*'})
@register_api("rsi/org")
def getOrgInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarCitizen API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)

    logging.info("Action requested: org")
    if not 'q' in qs:
        return '{"error":"missing query string"}'
    query = qs['q'][0]
    result = rsi.getOrgInfo(query)
    return json.dumps(result)

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'*'})
@register_api("rsi/citizen")
def getCitizenInfo(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarCitizen API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)

    logging.info("Action requested: citizen")
    if not 'q' in qs:
        return '{"error":"missing query string"}'
    query = qs['q'][0]
    result = rsi.getCitizenInfo(query)
    return json.dumps(result)

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'*'})
@register_api("rsi/citizen/search")
def searchCitizen(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for rsi API"}'
    if query == "":
        return '{"error":"empty query"}'
    qs = cgi.parse_qs(query)
    if not 'q' in qs:
        return '{"error":"missing query string"}'
    query = qs['q'][0]
    result = rsi.searchCitizen(query)
    return json.dumps(result)

@set_headers({'Content-Type':'application/json','Access-Control-Allow-Origin':'*'})
@register_api("rsi/news")
def getNews(query):
    global has_config
    if not has_config:
        return '{"error":"No configuration loaded for StarCitizen API"}'

    #{channel: "", series: "", type: "", text: "", sort: "publish_new", page: 7}
    data = {
        "channel": "",
        "series": "",
        "type": "",
        "text": "",
        "sort": "publish_new",
        "page": "1"
    }
    if(query):
        print(query)
        qs = cgi.parse_qs(query)
        print(qs)
        for k in data.keys():
            if k in qs:
                if k == "page":
                    data[k] = int(qs[k][0])
                else:
                    data[k] = qs[k][0]
    print(data)

    logging.info("Action requested: news")
    result = rsi.getNews(data)
    return json.dumps(result)