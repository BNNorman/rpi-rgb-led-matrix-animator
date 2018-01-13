#TextChainMaker.py

This program allows you to specify a text message, an XY offset for the top left corner and a font in order to produce a python list of XY coordinates for the letters.

This enables you to use the non-text animations on a text string.

Beware, if you select, for example, a 14pt font it will be rendered 14 LEDs high.

The program is written to read in BDF fonts only.

Note that the program cannot infer stroke start/end points from the BDF file. So, it generates LED co-ordinates based on the top left pixel and the supplied XY starting co-ordinates. The program only returns the co-ordinates of the pixels which should be set and ignores the background.

When the program ends it tells you how many pixels/leds the string occupies and provides you with a python list of the XY co-ordinates of the pixels. You can then use the list in your animation (See Main.py for an example)