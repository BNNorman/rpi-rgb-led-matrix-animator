# Fonts

This program currently only supports BDF and Hershey fonts. 

TODO: I believe that Using the python PIL library may enable the use of TrueType or OpenType fonts as well.

# Hershey

OpenCV uses Hershey fonts which are scaleable and may be drawn bold or italic. They can also be drawn using 
anti-aliasing (lineType=LINE_AA)

# BDF

Currently BDF (Bitmap distribution Format) fonts are not scaled so there has to be a font size matching the target 
size. See Constants.py for the list available.

Some bold and italic (Obtuse) BDF fonts exist in the Fonts folder. If you wish to use them then replace the 
appropriate font size in Constants.py. Since I didn't have an equivalent italic or bold, for each pixel size, 
available, I stuck with normal.

Currently BDF fonts are listed in a Python dictionary keyed by pixel size.

TODO: Code changes will be required to allow selection of bold/italic. I would recommend using thickness=2 for bold 
because Hershey fonts already have a **thickness** setting.

# Font Metrics

Fonts have ascenders and descenders. 

BDF font files report ascender+descender as the font size so a 9x18 font is 9 
pixels wide and 18 pixels tall split between 14 pixels ascending and 4 descending.

OpenCV Hershey fonts are rendered on the baseline. If you select a 13pt Hershey font then it occupies 13 pixels above
 the baseline and maybe 4 below. So a Hershey font of 13pt could be 17 pixels tall.
 
TODO: Code changes to change the hershey font scale so that 14pt Hershey looks the same size as 14pt BDF.

# BDF and Unicode text

You need to tell python 2 that you are using unicode encoding AND you need to specify your strings as unicode.

Place this at the start of your main.py

    # -*- coding: UTF-8 -*-

Then prefix your strings with 'u' like this:-

    myString=u"Some message with unicode characters in it like this:- €"

# Hershey and unicode

I haven't tested this but, apparently, unicode won't work with openCV unless it is compiled with Qt support. This is 
beyond the scope of this python based project. If you can get it going I'd like to hear from you so I can document how.

# TrueType/OpenType and PIL Fonts

In order to support OpenType/TrueType and PIL fonts PILFONT.Font.py is invoked when you specify a fontface (filename)
 which ends with .ttf or .otf or .pil
