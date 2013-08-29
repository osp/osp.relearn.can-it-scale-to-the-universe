#! /usr/bin/env python2

"""
Usage:
    gpx2hpgl.py <file.hpgl>
VS
de 1 a 42 cms par secondes
"""


from lxml import etree
import datetime
import math
import sys


NS = 'http://www.topografix.com/GPX/1/0'


def walk(tree):
    trkpts = tree.xpath('//gpx:trkpt', namespaces={'gpx': NS})

    for trkpt in trkpts:
        lon = float(trkpt.attrib['lon'])
        lat = float(trkpt.attrib['lat'])
        ele = trkpt.find('{%s}ele' % NS).text
        time = trkpt.find('{%s}time' % NS).text
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

        yield dict(lon=lon, lat=lat, ele=ele, time=time)

def main(f):
    f = open(f)
    tree = etree.parse(f)

    trkpts = list(walk(tree))

    min_lon = min(d['lon'] for d in trkpts)
    max_lon = max(d['lon'] for d in trkpts)
    min_lat = min(d['lat'] for d in trkpts)
    max_lat = max(d['lat'] for d in trkpts)

    hpgl = "IN\n"
    hpgl += "IP0,16158,0,11040;\n"
    hpgl += "SC%s,%s,%s,%s;\n" % (min_lon, max_lon, min_lat, max_lat)
    hpgl += "SP1;\n"
    hpgl += "PD;\n"

    for i, trkpt in enumerate(trkpts[1:]):
        #ab = trkpt['lon'] - trkpts[i]['lon']
        #bc = trkpt['lat'] - trkpts[i]['lat']
        #ac = math.sqrt(ab**2 + bc**2)
        #delta = trkpt['time'] - trkpts[i]['time']
        #hpgl += "VS%s;\n" % delta.seconds

        lon = (((trkpt['lon'] - min_lon) / (max_lon - min_lon)) * 1000)
        lat = (((trkpt['lat'] - min_lat) / (max_lon - min_lon)) * 1000)

        hpgl += "PA%s,%s;\n" % (lon, lat)

    hpgl += 'SP0;\n'

    print(hpgl)

if __name__ == "__main__":
    f = sys.argv[1]
    main(f)
