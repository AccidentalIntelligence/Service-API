import json
import logging
import urllib
import urllib2

from .. import config

def getStreamStatus(channel):
    url = "https://api.twitch.tv/kraken/streams/{0}?client_id={1}".format(channel, config.client_id)
    result = {}
    result['channel'] = channel
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['stream']:
            result['viewers'] = data['stream']['viewers']
            result['game'] = data['stream']['game'].encode('utf8')
            result['live'] = 1
            result['logo'] = data['stream']['channel']['logo']
            result['name'] = data['stream']['channel']['display_name']
            result['title'] = data['stream']['channel']['status']
        else:
            result['viewers'] = 0
            result['game'] = ""
            result['live'] = 0
            result['logo'] = ""
            result['name'] = ""
            result['title'] = ""
    except urllib2.URLError:
        return None
    return result

def getStreamCount():
    url = "https://api.twitch.tv/kraken/streams/?client_id={1}".format(config.client_id)

    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data._total:
            return data._total
        else:
            return 0

    except urllib2.URLError:
        return 0
