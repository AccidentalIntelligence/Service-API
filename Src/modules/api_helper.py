#has_config = {}
api_register = dict()
api_headers = dict()

def register_api(api):
    global api_register
    def wrap(func):
        # do pre-wrap
        print "Registering API: " + api
        def wrapped(query):
            return func(query)
        wrapped.func_name = func.func_name
        api_register[api] = wrapped
        return wrapped
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
