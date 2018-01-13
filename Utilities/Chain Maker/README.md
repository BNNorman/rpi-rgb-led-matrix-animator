**Chain Maker**

This program is provided with no warranty whatsover. It is freeware. If you can improve it (I'm sure you can) then please share back. All I ask is you let others know where you got it.

It's purpose is to take an SVG which has been marked up using named groups (layers) with LED positions and spit out python lists, containing the co-ordinates, which can be used with my Animation software.

When naming the layers take care to use to valid/non-conflicting variable names - you can change them later if need be.

ChainMaker.py uses the SVG drawing layers to form named chains which it outputs to a text file. These can then be used in the LED panel animations. The XY co-ordinates of the LEDs are rounded to the nearest whole number (you can't have half a LED). It removes duplicate XY pairs - since you can't have two LEDs in the same physical position. 

Get yourself a copy of Inkscape (free). Load in your image on the bottom layer. Decide which regions you want to animate independently and add layers for each region. Then stick a circle/ellipse where you want the LEDs to be. Oh, and follow the order you want the LEDs to be in your chain. If you want the animation to start on the left start marking the leds from the left - simple!

In inkscape, it makes life easier if you setup you page size to be the same physical dimensions and overlay a grid to show where the LEDs will go.

For example, if you use a 320mmx160mm LED panel setup your Inkscape page to 320x160mm in File->Document properties. My panels have 5mm LED spacing so I set the grid Spacing X and Y to 5 and a major grid line every 16. The grid lines don't affect how ChainMaker.py works. You will need to edit ChainMaker.py to tell it the dimensions of the LED panel in pixels.  

**Warning**

The UK football clubs are red hot about stopping people using their logos - you have been warned.
Shame really but they do make a lot of money from their franchises. I'm sure if you make a panel to hang on your bedroom wall they won't get to know but if you tried to go commercial - well, you have been warned.


**Edit ChainMaker.py**

Change the filename on this line to be the name of your marked up SVG :-

doc=minidom.parse('DAF_1.svg')

Change the filename on this line to be your output filename :-

fp=open("DAF LED.pos","w")

Personally, I have several copies of ChainMaker.py renamed and setup for different truck logos. It makes it easier to come back to - especially if panel sizes change between different panels.



**The Output**

Your output file will contain something like this .... note that I have butchered the lists so they are readable here.

CROSS=[(32, 25), (32, 27), (32, 29), (32, 30), (32, 32), ..... (33, 31), (31, 31)]
D=[(11, 13), (12, 12), (14, 11), (16, 10), (18, 10), (20, 11), ....., (16, 19), (15, 18), (13, 16), (12, 15)]
A=[(27, 18), (28, 16), (29, 14), (29, 12), (30, 11), (30, 9), (31, 7), ..... , (32, 14), (34, 14)]
F=[(42, 19), (43, 18), (44, 16), (45, 14), (45, 12), (46, 11), (47, 9), ..... (48, 16), (50, 17)]
OUTERRING=[(32, 21), (33, 21), (36, 21), (37, 22), (39, 23), ..., (27, 22), (29, 21)]
INNERRING=[(33, 24), (35, 24), (37, 25), ...... (27, 38), (26, 37), (25, 35), (24, 33), (29, 24), (31, 24)]
LEFTWING=[(5, 25), (5, 23), (3, 22), ..... (17, 26), (19, 26), (21, 26), (9, 28), (12, 28), (20, 30)]
RIGHTWING=[(59, 24), (59, 23),...(45, 26), (45, 30), (47, 30), (49, 30)]

You would copy and paste your lists into the Main.py of the animation program