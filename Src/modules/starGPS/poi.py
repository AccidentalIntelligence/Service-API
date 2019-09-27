

class poi:
    def __init__(self, name):
        self.name = name
        self.location = np.array([0,0,0])

    def geolocate(ranges):
        valid_markers = config.valid_markers
        if bool(ranges['OM1']) ^ bool(ranges['OM2']) and len(ranges.keys()) == 4:
            pass
        else:
            print "Error, either OM1 or OM2 are needed for geolocation"
            return np.array([0,0,0])
        

        