import json
import urllib2
import urllib

'''

https://robertsspaceindustries.com/api/starmap/bootup

data.species
data.systems.rowcount
data.systems.resultset[]
    .code
    .name
    .type
    .id
    .description

https://robertsspaceindustries.com/api/starmap/bookmarks/find
https://robertsspaceindustries.com/api/starmap/celestial-objects/SOL

data.resultset[].celestial_objects[]
    .type (PLANET)
    .affiliation
        .id
        .name
        .code
    .code
    .descirption
    .designation
    .habitable
    .id
    .name
    .subtype.name
    .sensor_danger
    .sensor_economy
    .sensor_population
    .thumbnail.source

https://robertsspaceindustries.com/api/starmap/celestial-objects/SOL.PLANETS.EARTH

.data.resultset[].children[]
    .type (LZ, SATELLITE)
    .code
    .description
    .designation
    .id

to load starmap: https://robertsspaceindustries.com/starmap?location=ELLIS.PLANETS.ELLISI&system=ELLIS

'''

def getSystems():
    url = "https://robertsspaceindustries.com/api/starmap/bootup"
    systems = {}
    try:
        res = urllib2.urlopen(url,"")
        data = json.load(res)["data"]

        for system in data['systems']['resultset']:


            sysdata = (
                system['code'],
                system['name'],
                system['description'],
                system['type'],
                system['id']
            )

            systems[system['code']] = sysdata
        logging.debug("Systems Added: " + ", ".join(systems.keys()))

    except:
        logging.error("Failed to load systems")
    return systems

def getPlanets(system):
    url = "https://robertsspaceindustries.com/api/starmap/star-systems/" + system
    print url
    try:
        res = urllib2.urlopen(url, "")
        data = json.load(res)["data"]["resultset"][0]
        affiliation = int(data['affiliation'][0]['id'])
        data = data['celestial_objects']
    except:
        logging.error("Failed loading URL")
        data = []
        affiliation = 0
    planets = {}
    for obj in data:
        if obj['type'] == "PLANET":
            planet = obj

            if planet['habitable']:
                planet['habitable'] = 1
            else:
                planet['habitable'] = 0
            if 'thumbnail' in planet.keys():
                planet['thumbnail'] = planet['thumbnail']['source']
            else:
                planet['thumbnail'] = ""
            try:
                planet['danger'] = int(planet['sensor_danger'])
                planet['economy'] = int(planet['sensor_economy'])
                planet['population'] = int(planet['sensor_population'])
            except:
                print "Failed conversion..."
                planet['danger'] = planet['economy'] = planet['population'] = 0

            planetData = (
                planet['code'],
                planet['name'],
                planet['description'],
                planet['subtype']['name'],
                planet['designation'],
                planet['habitable'],
                planet['danger'],
                planet['economy'],
                planet['population'],
                planet['thumbnail'],
                affiliation,
                system
            )
            planets[planet['code']] = planetData
            #c.execute(sql, planetData)
    logging.debug("Planets added: " + ", ".join(planets.keys()))
    return planets

def getCities(planet, system):
    url = "https://robertsspaceindustries.com/api/starmap/celestial-objects/" + planet
    print url
    try:
        res = urllib2.urlopen(url, "")
        data = json.load(res)["data"]["resultset"][0]
        data = data['children']
    except:
        print "Failed loading URL"
        data = []
    cities = {}
    for obj in data:
        # TODO: Add in check for moons and such...
        if obj['type'] == "LZ":
            city = obj

            cityData = (
                city['code'],
                city['name'],
                city['description'],
                planet,
                system
            )

            cities[city['code']] = cityData
    logging.debug("Cities added: " + ", ".join(cities.keys()))
    return cities