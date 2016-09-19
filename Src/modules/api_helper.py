
#has_config = {}
api_register = dict()

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
