#! /usr/bin/env python2

"""
VS
de 1 a 42 cms par secondes
"""


from lxml import etree
import datetime
import math


NS = 'http://www.topografix.com/GPX/1/0'
FACTOR = 1000000


hpgl = "IN\n"

f = open('pierreh-2013-08-28T153250.gpx')
tree = etree.parse(f)

trkpts = tree.xpath('//gpx:trkpt', namespaces={'gpx': NS})


min_lon = None
min_lat = None
max_lon = None
max_lat = None



for trkpt in trkpts:
    lon = float(trkpt.attrib['lon'])
    lat = float(trkpt.attrib['lat'])

    if lon < min_lon or min_lon is None:
        min_lon = lon

    if lon > max_lon or max_lon is None:
        max_lon = lon

    if lat < min_lat or min_lat is None:
        min_lat = lat

    if lat > max_lat or max_lat is None:
        max_lat = lat

min_lon = min_lon * FACTOR
min_lat = min_lat * FACTOR
max_lon = max_lon * FACTOR
max_lat = max_lat * FACTOR


#print(min_lon, max_lon, min_lat, max_lat)



trkpt = trkpts[0]

old_lon = float(trkpt.attrib['lon']) * FACTOR
old_lat = float(trkpt.attrib['lat']) * FACTOR

old_ele = trkpt.find('{%s}ele' % NS).text
old_time = trkpt.find('{%s}time' % NS).text
old_time = datetime.datetime.strptime(old_time, "%Y-%m-%dT%H:%M:%SZ")

hpgl += "IP0,16158,0,11040;\n"
hpgl += "SC%s,%s,%s,%s;\n" % (min_lon, max_lon, min_lat, max_lat)
hpgl += "SP1;\n"
hpgl += "PD;\n"


for trkpt in trkpts[1:]:
    lon = float(trkpt.attrib['lon']) * FACTOR
    lat = float(trkpt.attrib['lat']) * FACTOR
    ele = trkpt.find('{%s}ele' % NS).text
    time = trkpt.find('{%s}time' % NS).text
    time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    ab = lon - old_lon
    bc = lat - old_lat

    ac = math.sqrt(ab**2 + bc**2)

    time_delta = time - old_time
    hpgl += "VS%s;\n" % time_delta.seconds
    hpgl += "PA%s,%s;\n" % (lon,lat)

    old_lat = lat
    old_lon = lon
    old_ele = ele
    old_time = time

hpgl += 'SP0;\n'

print(hpgl)
