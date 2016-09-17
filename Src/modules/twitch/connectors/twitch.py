import json
import logging
import urllib
import urllib2

from .. import config

def getStreamStatus(channel):
    url = "https://api.twitch.tv/kraken/streams/{channel}?client_id={client_id}".format(channel=channel, client_id=config.client_id)
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

def getStreamAtOffset(game, offset):
    url = "https://api.twitch.tv/kraken/streams/?game={g}&limit=1&offset={offset}&client_id={client_id}".format(g=game, offset=offset, client_id=config.client_id)

    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        logging.debug(data)
        stream = data['streams'][0]['channel']
        if 'name' in stream:
            return getStreamStatus(stream['name'])
        else:
            return {"error":"Error getting random stream."}

    except urllib2.URLError:
        return {"error":"Unable to connect to Twitch API."}

def getStreamCount(game):
    url = "https://api.twitch.tv/kraken/streams/?game={g}&client_id={client_id}".format(g=game, client_id=config.client_id)

    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['_total']:
            return data['_total']
        else:
            return 0

    except urllib2.URLError:
        return 0
