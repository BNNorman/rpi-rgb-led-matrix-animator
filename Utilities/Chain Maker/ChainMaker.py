'''

ChainMaker.py used to create a python list of led positions for use
by the animator code

Copyright (C) 2017 Brian Norman, brian.n.norman@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''
from xml.dom import minidom
from SVGParser import *
import sys
import os

print "sys path=",sys.path[0]


src="DAF_640_640"


def simplify(xyList):
    # remove duplicate XY coords
    # need to keep first occurance

    newList=[]
    duplicatesRemoved=False
    for p in range(len(xyList)):
        x,y= xyList[p]
        if (x,y) not in newList:
            newList.append((x,y))
        else:
            duplicatesRemoved=True

    if duplicatesRemoved:
        print "  Duplicates removed"
    return newList



print "ChainMaker.py starting"
file=os.path.join(sys.path[0],src+".svg")
doc=minidom.parse(file)

parser=SVGParser(64,64)     # co-ords scaled to fit inside 64x64 matrix, aspect ratio is always maintained
parser.parse(doc)
layers=parser.getLayers() # dictionary for named layers

file=os.path.join(sys.path[0],src+".py")
fp=open(file,"w")

for key in layers:
    print("Processing layer for",key)
    fp.write(key+"="+str(simplify(layers[key]))+"\n")
fp.close()

print "chains written to ",file