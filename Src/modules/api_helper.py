from config import config
#has_config = {}
api_register = dict()
api_headers = dict()

def register_api(api):
    global api_register
    def wrap(func):
        # do pre-wrap
        if api in config['available_apis']:
            print "Registering API: " + api
            def wrapped(query):
                return func(query)
            wrapped.func_name = func.func_name
            api_register[api] = wrapped
            return wrapped
        else:
            return None
        # do post-wrap
    return wrap

def set_headers(headers):
    global api_headers
    def wrap(func):
        print "Adding headers: " + str(headers)
        def wrapped(query):
            return func(query)
        wrapped.func_name = func.func_name
        api_headers[func] = headers
        return wrapped
    return wrap

def auth_request(key):
    #TODO: Add in API key check here...
    if not key:
        return False
    else:
        return True