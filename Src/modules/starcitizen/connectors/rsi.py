import json
import logging
from requests import get
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
    data = bs_parse(html, baseurl)
    return data

    
def bs_parse(html, baseurl):
    parsed = {}
    html = BeautifulSoup(html, 'html.parser')
    
    for div in html.select('div'):
        if div.get('id') == 'organization':
            parsed['name'] = div.h1.get_text().split("/").rstrip()

            for d in div.select('div'):
                if 'banner' in d['class']:
                    parsed['banner'] = baseurl + d.img['src']
                
                if 'logo' in d['class']:
                    parsed['logo'] = baseurl + d.img['src']
                    parsed['count'] = d.span.text.split(" ")[0]

                if 'body' in d['class']:
                    parsed['bio'] = d.get_text()

    return parsed

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

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (
        resp.status_code == 200
        and content_type is not None
        and content_type.find('html') > -1
    )
