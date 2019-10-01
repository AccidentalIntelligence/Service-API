import MySQLdb

from config import config

def get_system(name):
    # Get basic system info
    db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM systems WHERE name=%s", (name,))
    res = c.fetchall()
    return res
    # Get system locations

def get_location(name):
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
    location["POIs"] = POIs

    return location