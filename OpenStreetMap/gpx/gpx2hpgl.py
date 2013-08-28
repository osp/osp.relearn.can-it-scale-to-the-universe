"""
VS
de 1 a 42 cms par secondes
"""


from lxml import etree
import datetime
import math

hpgl = "IN\n"
FACTOR = 100000


NS = 'http://www.topografix.com/GPX/1/0'

f = open('pierreh-2013-08-28T153250.gpx')
tree = etree.parse(f)

trkpts = tree.xpath('//gpx:trkpt', namespaces={'gpx': NS})


trkpt = trkpts[0]

shift_x = 200
shift_y = 200
old_lon = float(trkpt.attrib['lon'])
old_lat = float(trkpt.attrib['lat'])

old_ele = trkpt.find('{%s}ele' % NS).text
old_time = trkpt.find('{%s}time' % NS).text
old_time = datetime.datetime.strptime(old_time, "%Y-%m-%dT%H:%M:%SZ")

hpgl += "IP%s,%s;\n" % (str(old_lon).replace('.', ','), str(old_lon).replace('.', ','))
hpgl += "SC1488,0,0,1052;\n"
hpgl += "SP1;\n"


for trkpt in trkpts[1:]:
    lon = float(trkpt.attrib['lon'])
    lat = float(trkpt.attrib['lat'])
    ele = trkpt.find('{%s}ele' % NS).text
    time = trkpt.find('{%s}time' % NS).text
    time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    ab = lon - old_lon
    bc = lat - old_lat

    ac = math.sqrt(ab**2 + bc**2)

    time_delta = time - old_time
    hpgl += "VS%s,%s;\n" % (time_delta.seconds, time_delta.microseconds)
    hpgl += "PA%s,%s;\n" % (str(lon).replace('.', ','), str(lat).replace('.', ','))

    old_lat = lat
    old_lon = lon
    old_ele = ele
    old_time = time

hpgl += 'PU;\n'

print(hpgl)
