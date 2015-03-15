import httplib2
from urllib import urlencode
import json
import logging

import types

# Service Configuration
api_url = "http://www.outpan.com/api/get_product.php?"
api_key = "008ec8d190294efc3cd0f7188f836b2a"

def getType(data):
    if 'Manufacturer' in data:
        return types.EQUIPMENT
    if 'Publisher' in data:
        return types.BOOK
    if 'Volume' in data:
        return types.CONSUMABLE
    return 0

def getBarcodeData(code):
    global api_key, format, num_days, include_location, api_url

    logging.info("Retrieving barcode data from outpan")
    logging.info("Using code: "+code)

    barcodeData = {}
    barcodeData['code_id'] = code

    # Grab data for location
    data = dict()
    data['barcode'] = code
    data['apikey'] = api_key

    http = httplib2.Http()

    response, content = http.request(api_url+urlencode(data))

    print content;

    error = False

    if 'error' in content:
        error = True

    if error:
        barcodeData['type'] = 0
        return barcodeData

    print "no error!"
    data = json.loads(content)['attributes']
    print data

    barcodeData['type'] = getType(data);

    return barcodeData
