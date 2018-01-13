#Fonts

This program currently only supports BDF and Hershey fonts. 

TODO: I believe that Using the python PIL library may enable the use of TrueType or OpenType fonts as well. This 
would require the definition of a constant like TTF_FONTTYPE or OTF+FONTTYPE in Constants.py. Then create a folder 
(TTF/OTF) and add a Fonts.py file to it - see the OPENCV folder for an example.

#Hershey

OpenCV uses Hershey fonts which are scaleable and may be drawn bold or italic. They can also be drawn using 
anti-aliasing (lineType=LINE_AA)

#BDF

Currently BDF (Bitmap distribution Format) fonts are not scaled so there has to be a font size matching the target 
size. See Constants.py for the list available.

Some bold and italic (Obtuse) BDF fonts exist in the Fonts folder. If you wish to use them then replace the 
appropriate font size in Constants.py. Since I didn't have an equivalent italic or bold, for each pixel size, 
available, I stuck with normal.

Currently BDF fonts are listed in a Python dictionary keyed by pixel size.

TODO: Code changes will be required to allow selection of bold/italic. I would recommend using thickness=2 for bold 
because Hershey fonts already have a **thickness** setting.

#Font Metrics

Fonts have ascenders and descenders. 

BDF font files report ascender+descender as the font size so a 9x18 font is 9 
pixels wide and 18 pixels tall split between 14 pixels ascending and 4 descending.

OpenCV Hershey fonts are rendered on the baseline. If you select a 13pt Hershey font then it occupies 13 pixels above
 the baseline and maybe 4 below. So a Hershey font of 13pt could be 17 pixels tall.
 
TODO: Code changes to change the hershey font scale so that 14pt Hershey looks the same size as 14pt BDF.


 
