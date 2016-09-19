
has_config = False
api_register = dict()

def check_config():
    global has_config
    if has_config:
        return True
    else

def register_api(api):
    global api_register
    def wrap(func):
        # do pre-wrap
        print "Registering API: " + api
        def wrapped(query):
            global has_config
            if has_config:
                return func(query)
            else:
                return '{"error":"Configuration not loaded for API: '+api+'"}'
        wrapped.func_name = func.func_name
        api_register[api] = wrapped
        return wrapped
        # do post-wrap
    return wrap
