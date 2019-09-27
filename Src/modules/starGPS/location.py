

'''
A location is any planet, moon or other body where we may want to record POI's
'''

class location:
    def __init__(self, name, bounds):
        self.name = name
        self.bounds = bounds
        self.markers = [
            Marker("OM1", config.om_offset['OM1']['x'] * bounds, config.om_offset['OM1']['y'] * bounds, config.om_offset['OM1']['x'] * bounds),
            Marker("OM2", OM2[0] * bounds, OM3[1] * bounds, OM3[2] * bounds),
            Marker("OM3", OM3[0] * bounds, OM3[1] * bounds, OM3[2] * bounds),
            Marker("OM4", OM4[0] * bounds, OM3[1] * bounds, OM3[2] * bounds),
            Marker("OM5", OM5[0] * bounds, OM3[1] * bounds, OM3[2] * bounds),
            Marker("OM6", OM6[0] * bounds, OM3[1] * bounds, OM3[2] * bounds)
        ]
        self.POIs = [
            
        ]

    def om_loc(self, marker, axis):
        loc = 