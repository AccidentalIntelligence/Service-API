import httplib2
from urllib import urlencode
import json
import logging

try:
    from .. import config
except ImportError:
    pass

# Service Configuration
fmt = "json"

def getWeatherData(location):
    global fmt

    logging.info("Retrieving weather data from WWO")
    logging.info("Using Location: "+location)
    # Grab data for location
    data = dict()
    data['q'] = location
    data['extra'] = 'localObsTime'
    data['num_of_days'] = config.num_days
    data['includeLocation'] = config.include_location
    data['format'] = fmt
    data['key'] = config.api_key

    http = httplib2.Http()

    print urlencode(data)

    response, content = http.request(config.api_url+urlencode(data))

    data = json.loads(content)['data']

    weatherData = {"current":{},"forecast":[]}
    weatherData['locationName'] = location
    current = data['current_condition'][0]
    forecast = data['weather']

    # current weather
    weatherData['current']['temp'] = current['temp_F']
    weatherData['current']['windSpeed'] = current['windspeedKmph']
    weatherData['current']['windDir'] = current['winddir16Point']
    weatherData['current']['precipMM'] = current['precipMM']
    weatherData['current']['humidity'] = current['humidity']
    weatherData['current']['visibility'] = current['visibility']
    weatherData['current']['pressure'] = current['pressure']
    weatherData['current']['cloud'] = current['cloudcover']

    # forecast weather
    i = 0
    for day in forecast:
        weatherData['forecast'].append({})
        weatherData['forecast'][i]['date'] = day['date']
        weatherData['forecast'][i]['tempMax'] = day['tempMaxF']
        weatherData['forecast'][i]['tempMin'] = day['tempMinF']
        weatherData['forecast'][i]['windSpeed'] = day['windspeedKmph']
        weatherData['forecast'][i]['windDir'] = day['winddir16Point']
        weatherData['forecast'][i]['precipMM'] = day['precipMM']
        weatherData['forecast'][i]['description'] = day['weatherDesc'][0]['value']
        i = i + 1

    return weatherData
