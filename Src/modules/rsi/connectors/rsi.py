import json
import logging
from requests import get
from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


try:
    from .. import config
except ImportError:
    pass


def getOrgInfo(sid):
    baseurl = "https://robertsspaceindustries.com"

    html = simple_get(baseurl + '/orgs/' + sid)
    if html:
        data = bs_parse_org(html, baseurl)
    else:
        data = {"Error": "Org not found."}
    return data

def getCitizenInfo(name):
    baseurl = "https://robertsspaceindustries.com"

    html = simple_get(baseurl + '/citizens/' + name)
    if html:
        data = bs_parse_citizen(html, baseurl)
    else:
        data = {"Error": "Citizen not found."}
    return data

def getNews():
    baseurl = "https://robertsspaceindustries.com"

    html = simple_post(baseurl + '/api/hub/getSeries')

    if html:
        data = json.loads(html)
    else:
        data = {"Error": "Couldn't fetch news."}
    return getNewsItems()
    #return data['data']

def getNewsItems():
    baseurl = "https://robertsspaceindustries.com"

    data = {"channel": "","series":"","type":"","text":"","sort":"publish_new","page":1}

    res = simple_post(baseurl + "/api/hub/getCommlinkItems", data)

    if res:
        return bs_parse_news(json.loads(res)['data'], baseurl)
    else:
        return "Failed"

    
def bs_parse_org(html, baseurl):
    parsed = {}
    html = BeautifulSoup(html, 'html.parser')
    
    for div in html.select('div'):
        if div.get('id') == 'organization':
            parsed['name'] = div.h1.get_text().split("/")[0].rstrip()

            for d in div.select('div'):
                if 'banner' in d['class']:
                    parsed['banner'] = baseurl + d.img['src']
                
                if 'logo' in d['class']:
                    parsed['logo'] = baseurl + d.img['src']
                    parsed['count'] = d.span.text.split(" ")[0]

                if 'body' in d['class']:
                    parsed['bio'] = d.get_text()

    return parsed

def bs_parse_citizen(html, baseurl):
    parsed = {}
    html = BeautifulSoup(html, 'html.parser')
    
    for div in html.select('div'):
        if div.get('id') == 'public-profile':

            for d in div.select('div'):
                if 'profile-content' in d.get('class'):
                    parsed['CitizenNo'] = d.p.string.text
                
                if 'thumb' in d.get('class'):
                    parsed['logo'] = baseurl + d.img['src']

                if 'body' in d['class']:
                    parsed['bio'] = d.get_text()

    return parsed

def bs_parse_news(html, baseurl):
    parsed = {}
    print html
    soup = BeautifulSoup(html, 'html.parser')
    print soup
    return soup

def simple_get(url):
    print url
    try:
        with closing(get(url, stream=True)) as resp:
            print resp
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        logging.error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def simple_post(url, data={}):
    print url
    try:
        with closing(post(url, data=data, stream=True)) as resp:
            print resp
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        logging.error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    print content_type
    return (
        resp.status_code == 200
        and content_type is not None
        and (content_type.find('html') > -1 or content_type.find('json') > -1)
    )
