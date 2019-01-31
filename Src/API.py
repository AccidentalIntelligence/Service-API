from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import time
import sys
import logging

import modules.weather.api as weather
import modules.twitch.api as twitch
import modules.citizen_register.api as register
import modules.badrolls.api as badrolls

from modules.api_helper import *

import config

def send404(handler, path):
    sendResponse(handler, 404, {'Content-Type':'application/xml'}, "<error>Path Error: /"+path+"</error>")
    return

def sendResponse(handler, code, headers, data):
    handler.send_response(code)
    items = headers.items()
    for item in items:
        handler.send_header(item[0], item[1])
    handler.end_headers()
    handler.wfile.write(data)
    return

def check_api(path, name):
    if path.endswith(name) and name in available_apis:
        return True
    return False

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        query = ""
        if path.find("?") > 0:
            query = path[path.index("?")+1:]
            path = path[0:path.index("?")].lstrip('/')
        try:
            if path in config.available_apis:
                api = api_register[path]
                sendResponse(self, 200, api_headers[api], api(query))
                return
            else:
                send404(self, path)
                return
        except IOError as details:
            self.send_error(404, 'IOError: '+str(details))


    def do_POST(self):
        pass


class APIServer(ThreadingMixIn, HTTPServer):
    def __init__(self, port):
        HTTPServer.__init__(self, ('',port), MyHandler)


def main(argv):
    logging.basicConfig(filename=config.log_file, format=config.log_format, datefmt=config.log_date_format, level=config.log_level)

    try:
        server = APIServer(config.port)
        if config.ssl:
            server.socket = ssl.wrap_socket (server.socket, keyfile=config.ssl_key, certfile=config.ssl_cert, server_side=True)
            logging.info('Started SSL API Server on port: ' + str(config.port))
        else:
            logging.info('Started API Server on port: '+str(config.port))
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info('^C received, shutting down API server!')

if __name__ == '__main__':
    main(sys.argv[1:])
