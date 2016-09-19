import httplib2
from urllib import urlencode
import json
import cgi
import time
from xml.etree.ElementTree import Element, SubElement, tostring
import MySQLdb
import logging

# check config can be loaded
try:
    import config
    has_config = True
except ImportError:
    has_config = False
    logging.debug("Cannot load config for the Weather API. The API will not function.")

# Connector. Change here to change remote service.
import connectors.wwo as connector

# Import dictionaries to format location names
from states import states
from countries import countries

def check_config():
    global has_config
    return has_config

def formatLocationName(area, region, country):
    global states, countries
    location = ""

    if country in countries:
        country = countries[country]

    # location in in the USA
    if region in states:
        region = states[region]

    location = ",".join([area, region, country])

    return location

def getSearchData(term):
    global has_config
    if !has_config:
        return {"error":"Weather API not configured!"}
    # trim the term to remove extraneous spaces, and convert to all uppercase
    term = ' '.join(term.split()).upper()

    #database connection
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)

    # First - check to see if we already have data for the search term
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("""SELECT * FROM search WHERE term = %s""", (term,))
    res = c.fetchall()
    searchData = []
    logging.debug("location search request received")

    if len(res) == 0:
        logging.debug("New terms, retrieving results from Weather API")
        # If not, perform the search
        data = dict()
        data['q'] = term
        data['format'] = 'json'
        data['key'] = config.api_key
        data['num_of_results'] = '5'

        http = httplib2.Http()
        response, content = http.request(config.search_url+urlencode(data))

        results = json.loads(content)
        if 'search_api' in results:
            results = results['search_api']['result']

            # Store the search data
            for result in results:
                locName = formatLocationName(
                    result['areaName'][0]['value'],
                    result['region'][0]['value'],
                    result['country'][0]['value']
                    )
                searchData.append(locName)

                c.execute("""INSERT INTO search (term, locationName) VALUES (%s, %s)""",(term, locName))
    else: # read results from the database
        logging.info("Results found in our Database")
        for result in res:
            #entry = dict()
            #entry['areaName'] = result['area']
            #entry['country'] = result['country']
            #entry['region'] = result['region']
            #searchData.append(entry)
            searchData.append(result['locationName'])

    db.close()
    # Return search results
    return searchData


def buildLocName(area, region, country):
    t = [area,region,country]
    name = ','.join(t)

def storeWeatherData(weatherData):
    #database connection
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    # Store current weather
    current = weatherData['current']
    c.execute(
    """INSERT INTO current (
            locationName,
            syncTime,
            temp,
            windSpeed,
            windDir,
            precipMM,
            humidity,
            visibility,
            pressure,
            cloud)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            weatherData['locationName'],
            time.time(),
            current['temp'],
            current['windSpeed'],
            current['windDir'],
            current['precipMM'],
            current['humidity'],
            current['visibility'],
            current['pressure'],
            current['cloud']))
    # Store forecast weather
    for day in weatherData['forecast']:
        c.execute(
        """INSERT INTO forecast (
                locationName,
                date,
                tempMax,
                tempMin,
                windSpeed,
                windDir,
                precipMM,
                description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                weatherData['locationName'],
                day['date'],
                day['tempMax'],
                day['tempMin'],
                day['windSpeed'],
                day['windDir'],
                day['precipMM'],
                day['description']))

    #database connection
    db.commit()
    db.close()
    return

def updateWeatherData(weatherData):
    global db

    logging.info('Updating stored data for location: '+weatherData['locationName'])
    #database connection
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    # update current data
    current = weatherData['current']
    c.execute(
    """UPDATE current SET
            syncTime = %s,
            temp = %s,
            windSpeed = %s,
            windDir = %s,
            precipMM = %s,
            humidity = %s,
            visibility = %s,
            pressure = %s,
            cloud = %s
            WHERE locationName = %s""", (
            time.time(),
            current['temp'],
            current['windSpeed'],
            current['windDir'],
            current['precipMM'],
            current['humidity'],
            current['visibility'],
            current['pressure'],
            current['cloud'],
            weatherData['locationName']))

    # update forecast data
    # clear it out first!
    c.execute("""DELETE FROM forecast WHERE locationName = %s""", (weatherData['locationName']))
    # then store the new data
    for day in weatherData['forecast']:
        c.execute(
        """INSERT INTO forecast (
                locationName,
                date,
                tempMax,
                tempMin,
                windSpeed,
                windDir,
                precipMM,
                description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                weatherData['locationName'],
                day['date'],
                day['tempMax'],
                day['tempMin'],
                day['windSpeed'],
                day['windDir'],
                day['precipMM'],
                day['description']))
    db.commit()
    db.close()
    return

def getWeatherData(location):
    global fmt, has_config
    if !has_config:
        return {"error":"Weather API not configured!"}
    # First - Check the database for Cached data
    #database connection
    db = MySQLdb.connect(host=config.dbhost,user=config.dbuser,passwd=config.dbpass,db=config.dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("""SELECT * FROM current WHERE locationName = %s""", (location,))
    res = c.fetchall()
    searchData = []
    weatherData = {}

    logging.info("Weather data request received for location: %s", location)
    if len(res) == 1:
        logging.info("Data found in DB for: %s", location)
        # Check database data is in-date
        if time.time() - float(res[0]['syncTime']) > 7200:#7200:
            logging.info("Data out of date for: %s", location)
            weatherData = connector.getWeatherData(location)

            #TODO: syncTime should be stored as an int?
            weatherData['current']['syncTime'] = str(time.time())
            updateWeatherData(weatherData)
        else:
            logging.info("Retrieving data from the Database")
            # Build weatherData from database data and return
            weatherData['locationName'] = location
            weatherData['current'] = res[0]
            weatherData['forecast'] = []
            # Get forecast data as well
            c.execute("""SELECT * FROM forecast WHERE locationName = %s""", (location,))
            res = c.fetchall()
            for row in res:
                weatherData['forecast'].append(row)
    elif len(res) == 0:
        print logging.info("Data not yet in in DB for: %s", location)
        weatherData = connector.getWeatherData(location)

        #TODO: syncTime should be stored as an int?
        weatherData['current']['syncTime'] = str(time.time())
        storeWeatherData(weatherData)

    else:
        print logging.critical("ERROR! More than one record? This shouldn't happen!")
    db.close()
    return weatherData


###[ XML generation code ]###########################################

def buildSearchResponse(searchData):
    # Data structure:
    # <searchData>
    #   <resultCount>xxx</resultCount> - Number of results returned
    #   <results>
    #       <resultItem>
    #           <areaName>xxx</areaName>
    #           <region>xxx</region>
    #           <country>xxx</country>
    #       </resultItem>
    #       <resultItem>
    #           ...
    #       </resultItem>
    #   </results>
    # </searchData>
    xml = Element('searchData')
    SubElement(xml, 'resultCount').text = str(len(searchData))
    resultsElement = SubElement(xml, 'results')
    for result in searchData:
        item = SubElement(resultsElement, 'resultItem').text = result
    return tostring(xml)


def buildWeatherResponse(weatherData):
    # data structure
    # <weatherData>
    #   <location>Dallas</location> - Location of weather data
    #   <syncTime>xxx</syncTime> - Time weather was last synchronized with the weather service in UTC
    #   <current>
    #       <temp>xxx</temp> - Temperature in Farenheit. Convert to Celcius locally
    #       <windSpeed>xxx</windSpeed> - Wind speed in km/h. Convert to mph locally
    #       <windDir>xxx</windDir> - Wind direction in degrees
    #       <precipMM>xxx</precipMM> - Precipitation in mm
    #       <humidity>xxx</humidity> - humidity in percentage
    #       <visibility>xxx</visibility> - visibility in kilometres
    #       <pressure>xxx</pressure> - Atmospheric pressure in millibars
    #       <cloud>xxx</cloud> - Cloud coverage in percentage
    #   </current>
    #   <forecast>
    #       <day>
    #           <date>xxx</date> - Date in YYYY-MM-DD format
    #           <tempMin>xxx</tempMin> - Minimum temperature in Farenheit. Convert to Celcius locally
    #           <tempMax>xxx</tempMax> - Maximum temperature in Farenheit. Convert to Celcius locally
    #           <windSpeed>xxx</windSpeed> - in km/h
    #           <windDir>xxx</windDir> - in degrees
    #           <precipMM>xxx</precipMM>
    #           <description>xxx</description> - description of forecasted weather
    #       </day>
    #       <day>
    #       </day>
    #   </forecast>
    # </weatherData>

    location = weatherData['locationName']
    current = weatherData['current']
    forecast = weatherData['forecast']
    xml = Element('weatherData')
    SubElement(xml, 'location').text = location
    SubElement(xml, 'syncTime').text = current['syncTime']
    # Current Weather
    currentElement = SubElement(xml, 'current')
    SubElement(currentElement, 'temp').text = current['temp']
    SubElement(currentElement, 'windSpeed').text = current['windSpeed']
    SubElement(currentElement, 'windDir').text = current['windDir']
    SubElement(currentElement, 'precipMM').text = current['precipMM']
    SubElement(currentElement, 'humidity').text = current['humidity']
    SubElement(currentElement, 'visibility').text = current['visibility']
    SubElement(currentElement, 'pressure').text = current['pressure']
    SubElement(currentElement, 'cloud').text = current['cloud']
    # Weather Forecast
    forecastElement = SubElement(xml, 'forecast')
    for item in forecast:
        day = SubElement(forecastElement, 'day')
        SubElement(day, 'date').text = item['date']
        SubElement(day, 'tempMin').text = item['tempMin']
        SubElement(day, 'tempMax').text = item['tempMax']
        SubElement(day, 'windSpeed').text = item['windSpeed']
        SubElement(day, 'windDir').text = item['windDir']
        SubElement(day, 'precipMM').text = item['precipMM']
        SubElement(day, 'description').text = item['description']
    return tostring(xml)

#####[ API Functions ]####################

def getSearchResponse(query):
    # Valid query string: q=search+query&u=userToken
    if query == "":
        return "<error>empty query</error>"
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return "<error>missing user token</error>"
    if not 'q' in qs:
        return "<error>missing query string</error>"
    result = getSearchData(qs['q'][0])
    if len(result) == 0:
        return "<error>No results found!</error>"
    return buildSearchResponse(result)

def getWeatherResponse(query):
    if query == "":
        return "<error>empty query</error>"
    qs = cgi.parse_qs(query)
    if not 'u' in qs:
        return "<error>missing user token</error>"
    if not 'q' in qs:
        return "<error>missing query string</error>"
    result = getWeatherData(qs['q'][0])
    return buildWeatherResponse(result)
