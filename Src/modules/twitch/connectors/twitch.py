import json
import logging
import urllib
import urllib2

# check config can be loaded
try:
    from ..config import config
except ImportError:
    pass

def getStreamStatus(channel):
    url = "https://api.twitch.tv/kraken/streams/{channel}".format(channel=channel)
    result = {}
    result['channel'] = channel
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        logging.debug(data)
        if data['stream']:
            result['viewers'] = data['stream']['viewers']
            if data['stream']['game']:
                result['game'] = data['stream']['game'].encode('utf8')
            else:
                result['game'] = 'None'
            result['live'] = 1
            result['channel'] = data['stream']['channel']['display_name']
            result['title'] = data['stream']['channel']['status']
            result['logo'] = data['stream']['channel']['logo']
        else:
            logging.info("Channel offline.")
            result['viewers'] = 0
            result['game'] = ""
            result['live'] = 0
            result['channel'] = ""
            result['title'] = ""
            result['logo'] = ""
    except urllib2.URLError:
        logging.error("Unable to get stream status for channel: " + channel)
        return None
    return result

def getStreamInfo(channel):
    url = "https://api.twitch.tv/kraken/channels/{channel}".format(channel=channel)
    result = {}
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if data['display_name']:
            if data['logo']:
                result['logo'] = data['logo']
            else:
                result['logo'] = "http://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_300x300.png"
            result['name'] = data['display_name']
        else:
            logging.info("Invalid channel specfied")
            result['logo'] = ""
            result['name'] = ""
    except urllib2.URLError:
        return None
    return result

def getStreamAtOffset(game, offset):
    url = "https://api.twitch.tv/kraken/streams/?game={g}&limit=1&offset={offset}".format(g=game, offset=offset)

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        stream = data['streams'][0]['channel']

        if 'name' in stream:
            return getStreamStatus(stream['name'])
        else:
            return {"error":"Error getting random stream."}

    except urllib2.URLError:
        logging.error("Could not get stream at offset")
        return {"error":"Unable to connect to Twitch API."}

def getStreamCount(game):
    url = "https://api.twitch.tv/kraken/streams/?game={g}".format(g=game)

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)

        if data['_total']:
            return data['_total']
        else:
            return 0

    except urllib2.URLError:
        logging.error("Could not request stream count")
        return 0
