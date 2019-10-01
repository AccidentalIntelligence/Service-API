from config import config

def get_system(name):
    # Get basic system info
    db = MySQLdb.connect(host=config['db']['host'], user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM channel_status WHERE channel=%s", (channel,))
    res = c.fetchall()

    # Get system locations

def get_location(name):
    # Get location info


    # Get sattelite locations


    # Get POIs
    pass