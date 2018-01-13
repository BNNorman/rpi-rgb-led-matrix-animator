'''
SVGParser class provides parsing of Inkscape SVG images and only Inkscape images.

It is used to extract ellipse/circle x-y co-ordinates , which mark approximate LED positions, from an SVG file and map
them onto an LED panel - adjusting LED coordinates to match the panel.

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
import re


class SVGParser:

        def __init__(self, width, height):
            self.panelWidth=width   # how many led wide
            self.panelHeight=height # how many leds tall
            self.dwgWidth=0
            self.dwgHeight=0
            self.layers={}
            self.curLayer=None
            self.scaling=1

        ################################################################################
        #
        # the only shape I'm interested in
        #
        #################################################################################

        def thumbnail(self,x,y):
            # two decimal places should be enough
            # the animation code does rounding
            return round(x*self.scaling,2),round(y*self.scaling,2)

        def processEllipse(self,node):
            cx = float(self.extractDimension(node.getAttribute('cx')))
            cy = float(self.extractDimension(node.getAttribute('cy')))

            if self.curLayer is None:
                print("No current layer")

            self.layers[self.curLayer]=self.layers[self.curLayer]+[self.thumbnail(cx,cy)]

        def extractDimension(self,dim):
            p=re.compile("(\d+\.?\d*)")
            m=p.match(dim)
            if m:
                return(m.group())
            else:
                print("Unable to match numerical dimension in",dim)
                return None

        # <g...>....</g>
        #
        # Each layer is processed as a separate python list
        #

        def processGroup(self,node):
            id = node.getAttribute('id')
            self.curLayer=node.getAttribute("inkscape:label")

            # new layer?
            if not self.curLayer in self.layers:
                self.layers[self.curLayer]=[]    # add a new layer with an empty list

            #print("processGroup layer=",self.curLayer)

            for child in node.childNodes:
                # ignore all others
                if child.localName == "ellipse":   self.processEllipse(child)
                if child.localName == "circle":    self.processEllipse(child)
                elif child.localName == "g": print("Nested group found whilst processing", self.curLayer)


        #########################################################################
        #
        # parse - called to decode the SVG document
        #
        #########################################################################
        def parse(self,doc):

            for child in doc.childNodes:

                if child.localName == "svg":
                    # process the drawing

                    # these values are used in thumbnailing to get the
                    # ellipse xy co-ordinates to fit the LED matrix

                    # WIDTH CAN BE PIXELS OR MM

                    self.dwgWidth = float(self.extractDimension(child.getAttribute('width')))
                    self.dwgHeight = float(self.extractDimension(child.getAttribute('height')))

                    vratio=self.panelHeight/self.dwgHeight
                    hratio=self.panelWidth/self.dwgWidth

                    # scale x & y by the same amount
                    # but make sure the resulting co-ordinates fit the panel
                    # by using the smaller ratio
                    self.scaling=vratio
                    if hratio<vratio: self.scaling=hratio

                    print("Scaling will be ",self.scaling)

                    nameSpace=child.getAttribute("xmlns:inkscape")

                    assert nameSpace is not None,"SVG document doesn't appear to be created by Inkscape."

                    # scan the child nodes
                    # inkscape defines at least one group

                    for sibling in child.childNodes:
                        # only interested in processing groups (layers)
                        if sibling.localName == "g":  self.processGroup(sibling)


        # used by the caller to get the resulting dictionary which contains the named
        # co-ordinate lists
        def getLayers(self):
            return self.layers