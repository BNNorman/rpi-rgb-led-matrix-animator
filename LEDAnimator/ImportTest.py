"""
CHECKS THAT MODULES CAN BE LOADED
"""

print "\nUtilLib import test"

from UtilLib import *
print "nearest 1.45=",nearest(1.45)


print "\nPalette import test"
from Palette import *

r=LOTS
print "LOTS length=",r.getLength()

print "\nBDF font import test"
from BDF import Font as bdf

f=bdf.Font(12)
print "hello world size=",f.getTextBbox("Hello world")

