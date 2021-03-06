import json
import logging
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
    .affiliation.name
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

Moon:

data.resultset[].celestial_objects[]
    .type (SATELLITE)
    .affiliation (empty, match parent?)
    .code
    .description
    .designation
    .habitable
    .id
    .name
    .subtype.name
    .sensor_danger
    .sensor_economy
    .sensor_population

LZs:

data.resultset[].celestial_objects[]
    .type (LZ)
    .affiliation (empty, match parent?)
    .code
    .description
    .designation
    .habitable
    .id
    .name (if empty, match designation?)
    .sensor_danger
    .sensor_economy
    .sensor_population

https://robertsspaceindustries.com/api/starmap/celestial-objects/SOL.PLANETS.EARTH

.data.resultset[].children[]
    .type (LZ, SATELLITE)
    .code
    .description
    .designation
    .id

to load starmap: https://robertsspaceindustries.com/starmap?location=ELLIS.PLANETS.ELLISI&system=ELLIS

'''

replaces = [
    (u"\u2019", "'"),
    (u"\u0101", "a"),
    (u"\u016b", "u"),
    (u"\u0113", "e")
]

def getSystems():
    url = "https://robertsspaceindustries.com/api/starmap/bootup"
    systems = {}
    #try:
    res = urllib2.urlopen(url,"")
    data = json.load(res)["data"]

    for system in data['systems']['resultset']:

        try:
            affiliation = int(system['affiliation'][0]['id'])
        except:
            affiliation = 0

        try:
            name = system['name']
            for rep in replaces:
                name = name.replace(rep[0], rep[1])
        except:
            name = system['name'].decode('ascii', 'ignore')

        try:
            description = system['description']
            for rep in replaces:
                description = description.replace(rep[0], rep[1])
        except:
            description = ""

        sysdata = (
            system['code'],
            name,
            affiliation,
            description,
            system['type'],
            system['id']
        )

        systems[system['code']] = sysdata
    logging.debug("Systems Added: " + ", ".join(systems.keys()))

    #except:
    #    logging.error("Failed to load systems")
    return systems

def getPlanets(system, sys_id):
    url = "https://robertsspaceindustries.com/api/starmap/star-systems/" + system
    print url
    try:
        res = urllib2.urlopen(url, "")
        data = json.load(res)["data"]["resultset"][0]
        affiliation = data['affiliation'][0]['name']
        data = data['celestial_objects']
    except:
        logging.error("Failed loading URL")
        data = []
        affiliation = 0
    planets = {}
    for obj in data:
        if obj['type'] == "PLANET" or obj['type'] == "SATELLITE":
            planet = obj
            if planet['affiliation']:
                local_affiliation = planet['affiliation'][0]['name']
            else:
                local_affiliation = affiliation
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

            if not planet['parent_id']:
                planet['parent_id'] = sys_id

            try:
                planet['id'] = int(planet['id'])
                planet['parent_id'] = int(planet['parent_id'])
            except:
                print "couldn't convert ids"

            if not planet['name']:
                planet['name'] = planet['designation']

            name = planet['name']
            for rep in replaces:
                name = name.replace(rep[0], rep[1])

            if planet['description']:
                description = planet['description']
                for rep in replaces:
                    description = description.replace(rep[0], rep[1])
            else:
                description = ""

            designation = planet['designation']
            for rep in replaces:
                designation = designation.replace(rep[0], rep[1])

            planetData = (
                planet['code'],
                name,
                description,
                planet['type'],
                planet['subtype']['name'],
                designation,
                planet['habitable'],
                planet['danger'],
                planet['economy'],
                planet['population'],
                planet['thumbnail'],
                local_affiliation,
                system,
                planet['id'],
                planet['parent_id']
            )
            planets[planet['code']] = planetData
            #c.execute(sql, planetData)
    logging.debug("Planets added: " + ", ".join(planets.keys()))
    return planets

def getCities(planet, parent_afill):
    url = "https://robertsspaceindustries.com/api/starmap/celestial-objects/" + planet
    print url
    try:
        res = urllib2.urlopen(url, "")
        data = json.load(res)["data"]["resultset"][0]
        if data['affiliation']:
            affiliation = data['affiliation'][0]['name']
        else:
            affiliation = parent_afill
        data = data['children']
    except urllib2.URLError as e:
        print "Failed loading URL"
        print e.reason
        data = []
    cities = {}
    for obj in data:
        # TODO: Add in check for moons and such...
        if obj['type'] == "LZ" or obj['type'] == 'MANMADE':
            city = obj

            if city['affiliation']: 
                local_affiliation = city['affiliation'][0]['name']
            else:
                local_affiliation = affiliation

            if city['habitable']:
                city['habitable'] = 1
            else:
                city['habitable'] = 0
            try:
                city['danger'] = int(city['sensor_danger'])
                city['economy'] = int(city['sensor_economy'])
                city['population'] = int(city['sensor_population'])
            except:
                print "Failed conversion..."
                city['danger'] = city['economy'] = city['population'] = 0

            if 'thumbnail' in city.keys():
                city['thumbnail'] = city['thumbnail']['source']
            else:
                city['thumbnail'] = ""

            if city['subtype']:
                city['subtype'] = city['subtype']['name']
            else:
                city['subtype'] = ""

            designation = city['designation']
            for rep in replaces:
                designation = designation.replace(rep[0], rep[1])

            if city['description']:
                description = city['description']
                for rep in replaces:
                    description = description.replace(rep[0], rep[1])
            else:
                description = ""

            try:
                city['id'] = int(city['id'])
                city['parent_id'] = int(city['parent_id'])
            except:
                print "couldn't convert ids"

            cityData = (
                city['code'], # code
                designation,
                city['type'],
                city['subtype'],
                description,
                city['habitable'],
                city['danger'], # danger
                city['economy'],# economy
                city['population'],# population
                city['thumbnail'], # thumbnail
                local_affiliation,
                planet,
                city['id'],
                city['parent_id']
            )

            cities[city['code']] = cityData
    logging.debug("Cities added: " + ", ".join(cities.keys()))
    return cities
