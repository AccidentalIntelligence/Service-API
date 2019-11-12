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

def getCitizenInfo(handle):
    baseurl = "https://robertsspaceindustries.com"

    html = simple_get(baseurl + '/citizens/' + handle)
    if html:
        data = bs_parse_citizen(html, baseurl)
        data['handle'] = handle
    else:
        data = {"Error": "Citizen not found."}
    return data

def searchCitizen(query):
    baseurl = "https://robertsspaceindustries.com"

    data = {
        'community_id': "1",
        'text': query
    }

    res = simple_post(baseurl + "/api/spectrum/search/member/autocomplete", data)

    print
    print(res)
    print

    if res:
        return json.loads(res)['data']

def getNews(data):
    baseurl = "https://robertsspaceindustries.com"

    #data = {"channel": "","series":"","type":"","text":"","sort":"publish_new","page":1}

    res = simple_post(baseurl + "/api/hub/getCommlinkItems", data)

    if res:
        return bs_parse_news(json.loads(res)['data'], baseurl)
    else:
        return "No Data"

    
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
                    parsed['record'] = d.p.strong.text

                if 'bio' in d['class']:
                    parsed['bio'] = d.div.get_text()
                
                if 'inner' in d['class']:
                    if d.p and d.p.span and d.p.span.text == "Enlisted":
                        parsed['enlisted'] = d.p.strong.get_text()

                if 'profile' in d['class']:
                    for d2 in d.select('div'):
                        if 'info' in d2['class']:
                            parsed['name'] = d2.p.strong.get_text()

                        if 'thumb' in d2['class']:
                            parsed['portrait'] = baseurl + d.img['src']
                
                if 'main-org' in d['class']:
                    for d2 in d.select('div'):
                        if 'thumb' in d2['class']:
                            parsed['org'] = d2.a.get('href').split('/')[2]
                        if 'info' in d2['class']:
                            for p in d2.select('p'):
                                if p.span and p.span.get_text() == "Organization rank":
                                    parsed['orgRank'] = p.strong.get_text()


    return parsed

def bs_parse_news(html, baseurl):
    parsed = []
    soup = BeautifulSoup(html, 'html.parser')

    for a in soup.select('a'):
        content = {}
        if a.get('href'):
            path = a.get('href')
            content['link'] = baseurl + path
            content['id'] = path.split('/')[3].split('-')[0]
        else:
            # skip articles with no link...
            continue
        for div in a.select("div"):
            if 'background' in div.get('class'):
                # Grab the image
                style = div.get('style')
                if style:
                    path = style.split("'")[1]
                    if path.startswith("http"):
                        content['image'] = path
                    else:
                        content['image'] = baseurl + style.split("'")[1]
                else:
                    content['image'] = baseurl + "/media/jkfgas4ihmfghr/channel_item_full/BookReport_FI_2.jpg"
            if 'title' in div.get('class'):
                content['title'] = div.get_text()
            if 'time_ago' in div.get('class'):
                content['posted'] = div.select("span")[0].get_text()
            
        parsed.append(content)
    return parsed

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        logging.error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def simple_post(url, data={}):
    try:
        with closing(post(url=url, data=data, stream=True)) as resp:
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
        and (content_type.find('html') > -1 or content_type.find('json') > -1)
    )
