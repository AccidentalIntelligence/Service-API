import httplib2
from urllib import urlencode
import json
import cgi
import time
from xml.etree.ElementTree import Element, SubElement, tostring
import MySQLdb
import logging

# Connector. Change here to change remote service.
import connectors.outpan as connector

# Import dictionaries to format location names
#from states import states
#from countries import countries

#search_url = "http://api.worldweatheronline.com/free/v1/search.ashx?"
#key = "nn9k24n22ndaxw3rw9e4wjzx"

# database params
dbhost = "localhost"
dbuser = "bcUser"
dbpass = "b4rc0de"
dbname = "barcode_service"

#####[ Validation Functoins ]#############

def validateBarcode(code):
    if len(code) < 12 or len(code) > 13:
        return False
    return True

#####[ Code data retrieval ]##############
def getBarcodeData(code):
    global key, search_url, dbhost,dbuser,dbpass,dbname

    result = {}

    if not validateBarcode(code):
        return result

    #database connection
    #db = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpass,db=dbname)

    # First - check to see if we already have data for the search term
    #c = db.cursor(MySQLdb.cursors.DictCursor)
    #c.execute("""SELECT * FROM codes WHERE code_id = %s""", (term,))
    #res = c.fetchall()
    res = []
    logging.debug("Barcode scan received")

    if len(res) == 0:
        logging.debug("New code, retrieving results from barcode API")
        # If not, perform the search
        result = connector.getBarcodeData(code)

        if 'code_type' in result and result['code_type'] != 0:
            pass
            # Store the search data
            #c.execute("""INSERT INTO codes (code_id, code_type) VALUES (%s, %s)""",(result['code_id'], result['code_type']))
    else: # read results from the database
        logging.info("Results found in our Database")


    #db.close()
    # Return search results
    return result

def storeBarcodeData(barcodeData):
    global dbhost,dbuser,dbpass,dbname
    #database connection
    db = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpass,db=dbname)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    # Store item
    c.execute(
    """INSERT INTO codes (
            code_id,
            code_type)
        VALUES (%s, %s)""", (
            barcodeData['code_id'],
            barcodeData['code_type']))

    #database connection
    db.close()
    return


###[ XML generation code ]###########################################

def buildScanResponse(data):
    # Data structure:
    # <data>
    #   <id>xxx</id> - Barcode scanned
    #   <type>xxx</type> - code type
    #   <description>xxx</description>
    # </data>
    response = dict()
    response['code'] = data['code_id']
    response['type'] = str(data['type'])
    return response



#####[ API Functions ]####################

def getScanResponse(query):
    # Valid query string: c=barcode
    result = [];
    if query == "":
        return {'error':'empty query'}
    qs = cgi.parse_qs(query)
    if not 'c' in qs:
        return {'error':'missing barcode'}
    if validateBarcode(qs['c'][0]):
        result = getBarcodeData(qs['c'][0])
    if len(result) == 0:
        return {'error':'No results found!'}
    return buildScanResponse(result)
