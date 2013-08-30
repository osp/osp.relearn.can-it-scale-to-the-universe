#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib2

from subprocess import call
import datetime


today1 = datetime.date.today()

print "If your body was"
print "the Artlibre Licence text"

## 
f = open("IYB_Artlibre_Manifesto1.txt")
txt = f.read()
f.close()

Manifesto = len(txt)

#len(IYB_Artlibre_Manifesto1.txt)
#SizeofLaws = len("IYB_Artlibre_Laws1.txt")

#Manifesto = urllib2.urlopen('http://artlibre.org/?print=Imprimer').read()
Licence = urllib2.urlopen('http://artlibre.org/licence/lal').read()

#factor1 = 10

#SizeofManifesto = len(Manifesto)
SizeofLicence = len(Licence)

print "Manifesto is " + str(Manifesto)
#print str(SizeofManifesto)
#print str(SizeofLicence)


SizeofLaw = str(SizeofLicence - Manifesto)

print "Licence is " + SizeofLaw

factor = .01

ManifestoSML = str(float(Manifesto) * factor)
SizeofLawSML = str(float(SizeofLaw) * factor)



Levels = """

beginfig(1)
draw (10,0) -- (20,0);
draw (10,""" + ManifestoSML + """) -- (20,""" + ManifestoSML + """);
draw (10,""" + SizeofLawSML + """) -- (20,""" + SizeofLawSML + """);
endfig;
end

"""
print Levels



## save Levels as an .mp file
g = open(Levels + '.mp', 'w')
g.write(IYB2)
g.close()

## and shell out to convert it to an image

command = str("mpost " + IYB2 + ".mp") # << this doesn't work

print command

call(IYB2, shell=True)  # << this works

print "		Success! you can now open somuchtosay.1 in evince"

