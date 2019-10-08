import MySQLdb
import json
import logging

from config import config

def get_system(name):
    try:
        # Get basic system info
        db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT * FROM systems WHERE name=%s", (name,))
        res = c.fetchall()[0]
        
        print res
        # Get system locations
        res['locations'] = []
        c.execute("SELECT name FROM systems WHERE parent=%s", (name,))
        locs = c.fetchall()
        for loc in locs:
            res['locations'].append(loc['name'])
        print res
        return res
    except MySQLdb.Error, e:
        
        logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if db:
            db.close()

    return 0

def get_location(name):
    try:
        # Get location info
        db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT * FROM locations WHERE name=%s", (name,))
        location = c.fetchall()[0]

        # Get sattelite locations
        location['sattelites'] = []

        # Get POIs
        db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT * FROM poi WHERE location=%s", (name,))
        POIs = c.fetchall()
        for poi in POIs:
            poi['coords'] = json.loads(poi['coords'])
        location["POIs"] = POIs

        return location
    except MySQLdb.Error, e:
        
        logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if db:
            db.close()

    return 0

def add_location(data):
    try:
        # Add location
        db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        c = db.cursor(MySQLdb.cursors.DictCursor)
        cols = sorted(data.keys())
        c.execute("INSERT INTO locations (" + ", ".join(cols) + ") VALUES (%(" + ")s, %(".join(cols) + ")s)", data)
        db.commit()
    except MySQLdb.Error, e:
        if db:
            db.rollback()
        
        logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if db:
            db.close()
    
    return 0

def add_poi(data):
    try:
        # Add location
        db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        c = db.cursor(MySQLdb.cursors.DictCursor)
        cols = sorted(data.keys())
        c.execute("INSERT INTO poi (" + ", ".join(cols) + ") VALUES (%(" + ")s, %(".join(cols) + ")s)", data)
        db.commit()
    except MySQLdb.Error, e:
        if db:
            db.rollback()
        
        logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if db:
            db.close()
    
    return 0