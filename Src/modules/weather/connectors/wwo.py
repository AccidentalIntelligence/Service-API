import httplib2
from urllib import urlencode
import json
import logging

# Service Configuration
api_url = "http://api.worldweatheronline.com/free/v1/weather.ashx?"
num_days = 5
include_location = "yes"
format = "json"
key = "nn9k24n22ndaxw3rw9e4wjzx"

def getWeatherData(location):
    global key, format, num_days, include_location, api_url
    
    logging.info("Retrieving weather data from WWO")
    logging.info("Using Location: "+location)
    # Grab data for location
    data = dict()
    data['q'] = location
    data['extra'] = 'localObsTime'
    data['num_of_days'] = num_days
    data['includeLocation'] = include_location
    data['format'] = format
    data['key'] = key
    
    http = httplib2.Http()
    
    print urlencode(data)
    
    response, content = http.request(api_url+urlencode(data))
    
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