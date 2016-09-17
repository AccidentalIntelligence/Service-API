from ..twitch import config

def getStreamStatus(channel):
    url = "https://api.twitch.tv/kraken/streams/{0}?client_id={1}".format(channel, config.client_id)
    result = {}
    result['channel'] = channel
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['stream']:
            result['viewers'] = data['stream']['viewers']
            result['game'] = data['stream']['game']
            result['live'] = 1
        else:
            result['viewers'] = 0
            result['game'] = ""
            result['live'] = 0
    except urllib2.URLError:
        return None
