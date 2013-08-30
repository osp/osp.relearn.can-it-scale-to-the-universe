#! /usr/bin/env python2

"""
Usage:
    ./gpx2hpgl.py <file.hpgl>
VS
de 1 a 42 cms par secondes

To test out: try to draw an A3 by walking around
try to use the grid on the floor in front of the house to reproduce drawings

+----------+
|       P2 |
|       +  |
|  :       |
|  :       |
|  :       |
|  +       |
| P1       |
+----------+
"""


import datetime
import math
import sys
from lxml import etree


#ISO A3 = 403.95mm x 276mm = 16158 units x 11040 units
WIDTH = 403.95  # mm
HEIGHT = 276  # mm

XMAX = 16158  # Remember we are working on A3
YMAX = 11040

MAX_VELOCITY = 41

assert (XMAX / WIDTH) == (YMAX / HEIGHT) 
mm = XMAX / WIDTH  # mm to plotter unit conversion


def walk(tree):
    ns = tree.getroot().nsmap[None]
    trkpts = tree.xpath('//gpx:trkpt', namespaces={'gpx': ns})

    for trkpt in trkpts:
        lon = float(trkpt.attrib['lon'])
        lat = float(trkpt.attrib['lat'])
        ele = trkpt.find('{%s}ele' % ns).text
        time = trkpt.find('{%s}time' % ns).text
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

        yield dict(lon=lon, lat=lat, ele=ele, time=time)


def velocities(trkpts):
    """
    l'anecdote du poteau en plus
    """
    for i, trkpt in enumerate(trkpts[1:]):
        ab = trkpt['lon'] - trkpts[i]['lon']
        bc = trkpt['lat'] - trkpts[i]['lat']
        ac = math.sqrt(ab**2 + bc**2)
        delta = trkpt['time'] - trkpts[i]['time']
        velocity = ac / delta.seconds
        yield velocity


def main(f):
    f = open(f)
    tree = etree.parse(f)

    trkpts = list(walk(tree))

    min_lon = min(d['lon'] for d in trkpts)
    max_lon = max(d['lon'] for d in trkpts)
    min_lat = min(d['lat'] for d in trkpts)
    max_lat = max(d['lat'] for d in trkpts)

    min_velocity = min([v for v in velocities(trkpts)])
    max_velocity = max([v for v in velocities(trkpts)])

    hpgl = "IN\n"
    hpgl += "IP0,%s,0,%s;\n" % (XMAX, YMAX)
    hpgl += "SC%s,%s,%s,%s;\n" % (0, XMAX / mm, 0, YMAX / mm)
    hpgl += "SP1;\n"
    hpgl += "PD;\n"

    for i, trkpt in enumerate(trkpts[1:]):
        ab = trkpt['lon'] - trkpts[i]['lon']
        bc = trkpt['lat'] - trkpts[i]['lat']
        ac = math.sqrt(ab**2 + bc**2)
        delta = trkpt['time'] - trkpts[i]['time']

        # From Roland's user manual:
        # Changing Maximum Plotting Speed The DIP switches on the back of the
        # DXY can be used to change the maximum plotting speed. When shipped
        # from the factory, maximum plotting speed is set at 420 mm
        # (16-9/16")/sec (all directions), but when set to [FAST] , maximum
        # plotting speed is 600 mm (23-5/8")/sec (45 degrees orientation).
        velocity = ac / delta.seconds
        velocity = (((velocity - min_velocity) / (max_velocity - min_velocity)) * MAX_VELOCITY) + 1

        hpgl += "VS%s;\n" % velocity

        # plot the first point
        if  i == 0:
            lon = (((trkpts[0]['lon'] - min_lon) / (max_lon - min_lon)) * XMAX) / mm
            lat = (((trkpts[0]['lat'] - min_lat) / (max_lon - min_lon)) * XMAX) / mm
            hpgl += "PA%s,%s;\n" % (lon, lat)

        lon = (((trkpt['lon'] - min_lon) / (max_lon - min_lon)) * XMAX) / mm
        lat = (((trkpt['lat'] - min_lat) / (max_lon - min_lon)) * XMAX) / mm

        hpgl += "PA%s,%s;\n" % (lon, lat)
        hpgl += "\n"

    hpgl += 'PU;\n'
    hpgl += 'SP0;\n'

    print(hpgl)

if __name__ == "__main__":
    try:
        f = sys.argv[1]
    except IndexError:
        print("Usage:\n    ./gpx2hpgl.py <file.hpgl>")
        sys.exit()
    main(f)
