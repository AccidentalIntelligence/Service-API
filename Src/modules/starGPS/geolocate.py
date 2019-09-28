import numpy as np
import math

# Class to hold orbital markers
class Marker:
    def __init__(self, name="unknown", x=0, y=0, z=0, r=0):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.range = r
        self.vec = np.array([x,y,z])

    def __str__(self):
        return "{0} - x:{1} y:{2} z:{3}".format(self.name, self.x,self.y,self.z)

###[ Config Values ]################################

bounds = 0 #distance between opposite OMs
markers = {}
om = []


# For Wolf Point. Target location: 776.2214, 510.0369
# [OM1, OM2, OM3, OM5]
#ranges = [455.5, 631.0,747.5,541.5]

####################################################

def distance(a, b):
    return np.linalg.norm(a - b)

def check_ranges(ranges):
    a = 0
    b = 0
    if len(ranges.keys()) > 6 or len(ranges.keys()) < 4:
        return False
    for r in ranges.keys():
        if r in ["OM1", "OM2"]:
            a = a + 1
        elif r in ["OM3", "OM4", "OM5", "OM6"]:
            b = b + 1
        else:
            return False
        if ranges[r] <= 0:
            return False
    if a < 1 or b < 3:
        return False
    return True


def init_markers(ranges):
    global om

    # Marker X/Y locations, relative to area size

    offsets = {
        'OM1': [0.5,0.5,1],
        'OM2': [0.5,0.5,0],
        'OM3': [0,0.5,0.5],
        'OM4': [1,0.5,0.5],
        'OM5': [0.5,0,0.5],
        'OM6': [0.5,1,0.5]
    }
    
    tmp = None

    for key in ranges.keys():
        m = Marker(key, offsets[key][0] * bounds, offsets[key][1] * bounds, offsets[key][2] * bounds, ranges[key])
        if key not in ["OM1", "OM2"]:
            om.append(m)
        else:
            tmp = m
    om.append(tmp)

    print "Orbital Markers:"
    for m in om:
        print "\t" + str(m)
    return True

def compute_circles():
    global om

    # Distance between orbital markers
    dist = [
        distance(om[1].vec, om[0].vec),
        distance(om[2].vec, om[1].vec),
        distance(om[0].vec, om[2].vec),
        ]

# X-distance of the two intersection points from the origin
    xa = (np.square(om[0].range) + np.square(dist[0]) - np.square(om[1].range)) / (2 * dist[0])
    xb = (np.square(om[1].range) + np.square(dist[1]) - np.square(om[2].range)) / (2 * dist[1])
    xc = (np.square(om[2].range) + np.square(dist[2]) - np.square(om[0].range)) / (2 * dist[2])

# Y-distance of the two intersection points from the origin
    ya = math.sqrt(np.square(om[0].range) - np.square(xa))
    yb = math.sqrt(np.square(om[1].range) - np.square(xb))
    yc = math.sqrt(np.square(om[2].range) - np.square(xc))

    if ya < 0:
        return "Circle A has no intersections"
    elif yb < 0:
        return "Circle B has no intersections"
    elif yc < 0:
        return "Circle C has no intersections"

# Unit Vectors
    exa = (om[1].x - om[0].x) / dist[0]
    exb = (om[2].x - om[1].x) / dist[1]
    exc = (om[0].x - om[2].x) / dist[2]

    eya = (om[1].y - om[0].y) / dist[0]
    eyb = (om[2].y - om[1].y) / dist[1]
    eyc = (om[0].y - om[2].y) / dist[2]

# Normal Vectors
    nxa = -eya
    nxb = -eyb
    nxc = -eyc

    nya = exa
    nyb = exb
    nyc = exc

# Calculate X and Y
    Q1xa = om[0].x + xa * exa
    Q1xb = om[1].x + xb * exb
    Q1xc = om[2].x + xc * exc

    Q1ya = om[0].y + xa * eya
    Q1yb = om[1].y + xb * eyb
    Q1yc = om[2].y + xc * eyc

    if (ya == 0 or yb == 0 or yc == 0):
        res = [
                [Q1xa, Q1ya],
                [Q1xa, Q1ya],
                [Q1xb, Q1yb],
                [Q1xb, Q1yb],
                [Q1xc, Q1yc],
                [Q1xc, Q1yc]
                ]
    else:
                
        Q2xa = Q1xa - ya * nxa
        Q2xb = Q1xb - yb * nxb
        Q2xc = Q1xc - yc * nxc

        Q2ya = Q1ya - ya * nya
        Q2yb = Q1yb - yb * nyb
        Q2yc = Q1yc - yc * nyc

        Q1xa += ya * nxa
        Q1xb += yb * nxb
        Q1xc += yc * nxc

        Q1ya += ya * nya
        Q1yb += yb * nyb
        Q1yc += yc * nyc

        try:
            ka = (Q2ya - Q1ya) / (Q2xa - Q1xa)
            da = Q2ya - (ka * Q2xa)
            yamax = ka * bounds + da
            yamin = ka * 0 + da
        except:
            yamax = float('nan')
            yamin = float('nan')

        try:
            kb = (Q2yb - Q1yb) / (Q2xb - Q1xb)
            db = Q2yb - (kb * Q2xb)
            ybmax = kb * bounds + db
            ybmin = kb * 0 + db
        except:
            ybmax = float('nan')
            ybmin = float('nan')

        try:
            kc = (Q2yc - Q1yc) / (Q2xc - Q1xc)
            dc = Q2yc - (kc * Q2xc)
            ycmax = kc * bounds + dc
            ycmin = kc * 0 + dc
        except:
            ycmax = float('nan')
            ycmin = float('nan')

        res = [
            {"x": Q1xa, "y": Q1ya},
            {"x": Q2xa, "y": Q2ya},
            {"x": Q1xb, "y": Q1yb},
            {"x": Q2xb, "y": Q2yb},
            {"x": Q1xc, "y": Q1yc},
            {"x": Q2xc, "y": Q2yc},
            {"x": yamax, "y": yamin},
            {"x": ybmax, "y": ybmin},
            {"x": ycmax, "y": ycmin}
            ]

    return res

def compute_lines(data):
    s1a = data[0]
    s2a = data[1]
    s1b = data[2]
    s2b = data[3]
    s1c = data[4]
    s2c = data[5]

# Directional vectors between Q1 and Q2 A
    vecA_x = s1a['x'] - s2a['x']
    vecA_y = s1a['y'] - s2a['y']
    vecAB_x = s1a['x'] - s1b['x']
    vecAB_y = s1a['y'] - s1b['y']

    vecB_x = s1b['x'] - s2b['x']
    vecB_y = s1b['y'] - s2b['y']
    vecBC_x = s1b['x'] - s1c['x']
    vecBC_y = s1b['y'] - s1c['y']

    vecC_x = s1c['x'] - s2c['x']
    vecC_y = s1c['y'] - s2c['y']
    vecCA_x = s1c['x'] - s1a['x']
    vecCA_y = s1c['y'] - s1a['y']

# Unit Vector
    vecA = math.sqrt(np.square(vecA_x) + np.square(vecA_y))
    exa = vecA_x / vecA
    eya = vecA_y / vecA

# Normal Vector
    normA_x = -eya
    normA_y = exa

# Unit Vector
    vecB = math.sqrt(np.square(vecB_x) + np.square(vecB_y))
    exb = vecB_x / vecB
    eyb = vecB_y / vecB

# Normal Vector
    normB_x = -eyb
    normB_y = exb

# Unit Vector
    vecC = math.sqrt(np.square(vecC_x) + np.square(vecC_y))
    exc = vecC_x / vecC
    eyc = vecC_y / vecC

# Normal Vector
    normC_x = -eyc
    normC_y = exc


    qx = vecAB_x * exa + vecAB_y * eya
    qy = vecAB_x * normA_x + vecAB_y * normA_y

    sx = exb * exa + eyb * eya
    sy = exb * normA_x + eyb * normA_y

    a = qx - qy * (sx / sy)

    xab = s1a['x'] - a * exa
    yab = s1a['y'] - a * eya

    qx = vecBC_x * exb + vecBC_y * eyb
    qy = vecBC_x * normB_x + vecBC_y * normB_y

    sx = exc * exb + eyc * eyb
    sy = exc * normB_x + eyc * normB_y

    b = qx - qy * (sx / sy)

    xbc = s1b['x'] - b * exb
    ybc = s1b['y'] - b * eyb

    qx = vecCA_x * exc + vecCA_y * eyc
    qy = vecCA_x * normC_x + vecCA_y * normC_y

    sx = exa * exc + eya * eyc
    sy = exa * normC_x + eya * normC_y

    c = qx - qy * (sx / sy)

    xca = s1c['x'] - c * exc
    yca = s1c['y'] - c * eyc

    loc = {
        'x': round(np.average([xab, xbc, xca]), 6),
        'y': round(np.average([yab, ybc, yca]), 6),
        'z': 0
    }

    return loc

def compute_z(loc):
    global markers
    '''
    Hypotenuse = range -> OM1
    A distance from target location to center of sphere
    '''
    center = bounds / 2
    if loc['x'] < center:
        xlen = center - loc['x']
    else:
        xlen = loc['x'] - center

    if loc['y'] < center:
        ylen = center - loc['y']
    else:
        ylen = loc['y'] - center
    
    len_a = np.sqrt(np.square(xlen) + np.square(ylen))
    len_h = om[3].range
    len_b = np.sqrt(np.square(len_h) - np.square(len_a))
    loc['z'] = round(bounds - len_b, 6)
    return loc

def fix_loc(loc):
    offset = bounds / 2
    _loc = {}
    _loc['x'] = loc['x'] - offset
    _loc['y'] = loc['y'] - offset
    _loc['z'] = loc['z'] - offset
    return _loc

def compute(data):
    global bounds
    bounds = data['bounds']

    if check_ranges(data['ranges']):
        init_markers(data['ranges'])
        d = compute_circles()
        d = compute_lines(d)
        loc = compute_z(d)
        loc = fix_loc(loc)
        return "Target is at coordinates = x:{0} y:{1} z:{2}".format(loc['x'], loc['y'], loc['z'])
    else:
        return "Invalid data sent!"