import json
import logging
import urllib
import urllib2

# check config can be loaded
try:
    from .. import config
except ImportError:
    pass

def getStreamStatus(channel):
    url = "https://api.twitch.tv/kraken/streams/{channel}?client_id={client_id}".format(channel=channel, client_id=config.client_id)
    result = {}
    result['channel'] = channel
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['stream']:
            result['viewers'] = data['stream']['viewers']
            if data['stream']['game']:
                result['game'] = data['stream']['game'].encode('utf8')
            else:
                result['game'] = 'None'
            result['live'] = 1
            result['channel'] = data['stream']['channel']['display_name']
            result['title'] = data['stream']['channel']['status']
        else:
            logging.info("Channel offline.")
            result['viewers'] = 0
            result['game'] = ""
            result['live'] = 0
            result['channel'] = ""
            result['title'] = ""
    except urllib2.URLError:
        return None
    return result

def getStreamInfo(channel):
    url = "https://api.twitch.tv/kraken/channels/{channel}?client_id={client_id}".format(channel=channel, client_id=config.client_id)
    result = {}
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['display_name']:
            result['logo'] = data['logo']
            result['name'] = data['display_name']
        else:
            logging.info("Invalid channel specfied")
            result['logo'] = ""
            result['name'] = ""
    except urllib2.URLError:
        return None
    return result

def getStreamAtOffset(game, offset):
    url = "https://api.twitch.tv/kraken/streams/?game={g}&limit=1&offset={offset}&client_id={client_id}".format(g=game, offset=offset, client_id=config.client_id)

    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
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
