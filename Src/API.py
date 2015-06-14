from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import modules.weather.api as weather
import modules.bcw.api as barcode
import time
import sys
import logging

port = 8396
log_file = "service.log"
log_format = '%(asctime)s:%(levelname)s:%(message)s'
log_date_format = '%Y/%m/%d-%I:%M:%S'
log_level = logging.DEBUG

def syncTime():
    result = "<time>"+str(time.time())+"</time>"
    return result

def send404(handler, path):
    sendResponse(handler, 404, {'Content-Type':'application/xml'}, "<error>Path Error: "+path+"</error>")
    return

def sendResponse(handler, code, headers, data):
    handler.send_response(code)
    items = headers.items()
    for item in items:
        handler.send_header(item[0], item[1])
    handler.end_headers()
    handler.wfile.write(data)
    return

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        query = ""
        if path.find("?") > 0:
            query = path[path.index("?")+1:]
            path = path[0:path.index("?")]
        try:
            if path.endswith("search"):
                sendResponse(self, 200, {'Content-Type':'application/xml'}, weather.getSearchResponse(query))
                return
            elif path.endswith("sync"):
                sendResponse(self, 200, {'Content-Type':'application/xml'}, syncTime())
                return
            elif path.endswith("weather"):
                sendResponse(self, 200, {'Content-Type':'application/xml'}, weather.getWeatherResponse(query))
                return
            elif path.endswith("code"):
                sendResponse(self, 200, {'Content-Type':'application/json'}, barcode.getScanResponse(query))
                return
            else:
                send404(self, path)
                return
        except IOError as details:
            self.send_error(404, 'IOError: '+str(details))


    def do_POST(self):
        pass


class APIServer(HTTPServer):
    def __init__(self, port):
        HTTPServer.__init__(self, ('',port), MyHandler)


def main(argv):
    global port
    logging.basicConfig(filename=log_file, format=log_format, datefmt=log_date_format, level=log_level)

    try:
        server = APIServer(port)
        logging.info('Started API Server on port: '+str(port))
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info('^C received, shutting down API server!')

if __name__ == '__main__':
    main(sys.argv[1:])