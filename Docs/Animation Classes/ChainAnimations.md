# Chain Animations

A chain is just a python list of X,Y co-ordinates. There can be multiple chains on an RGB LED Panel forming any shape 
you wish. There are a couple of utilities for creating chains from an image or text message. Look in the utilities 
folder.

Chains are stored in 3 numpy arrays: xList,yList and hsva (HSV colour space with alpha). xList and yList are the 
coordinates of the LED.

A chain can have an overall brightness and transparency multiplication factors which are applied to the chain when 
rendering for output. This means that the LEDs in a chain can have individual brightness/transparency which are not 
affected thus allowing a revert to original caopability.

The results of your animation are rendered into a chain buffer then output to the panel.

## Using Chain Animation Sequences

Here is a chain:-

`MyChain=[(59, 32), (59, 31), (61, 30), (63, 31), (62, 33), (61, 34), (60, 34), (59, 34), (57, 34), (55, 34), (53,
     34), (51, 34), (49, 34), (48, 34),]  `

You use it with an animation like this:-

`A.addAnimation(chain=Chain(MyChain,antiAliasMethod="wu"),seq=MySeq)`

If you don't specify an **antiAliasMethod** the chain will not be anti-aliased which is fine if the pixels all lie on 
integer XY coordinates like the example and forms a straight horizontal or vertical line. For other shapes it is better
 to specify an anti-alias method. The Wu method creates fewer pixels and so should be faster.

Currently only two anti-alias methods are available. See Helpers/AntiAlias.py for details.

## Chain Utilities

Creating chains by hand is tedious. There are three ways to create more complex chains.
- use the Helper/Chains.py routines to create (filled) circles, and (filled) rectangles
- use the Utilities/ChainMaker.py in conjuntion with InkScape to mark up led positions on an image.
- use the Utilities/TextChainMaker.py to generate a chain for a text message

## The Hardware and Software

Raspberry Pi 3 (not yet tried on zero ,2 or 1 since the model 3 is faster). It is running Raspbian Lite (Rasbian Stretch has just come out but I haven't tried it yet)to try to give the program as much CPU time as possible. Rasbian Lite doesn't start up a GUI. You will need to install hzellers driver code.

HUB75 interface - I used the adapter designed by hzeller. You can order 3 of the PCBs from OSHPark (https://oshpark.com/shared_projects/bFtff2GR - the price was very reasonable for 3 boards, free delivery and they keep you informed by email as the boards are being made.) - I recommend you go for the Active design as it level shifts the 3.3v Pi GPIO to the 5v required by the HUB75 panels. Make sure you buy the exact components specified - they work a treat. I got mine from Amazon/Ebay. Practise some SMD soldering before you build the boards. The technique is to solder down one leg first and when the component is in the correct place solder the rest. Sometimes drag soldering works well but you may need to use a solder sucker to remove any excess.

RGB Panels - I got mine from AlieExpress ( Shenzhen Lightall Optoelectronics Co., LTD). They came with power cables and two hub75 ribbon cables. They seem to be well made and are, basically two 32x32 panels. I bought the P5 (5mm spacing) panels as I wasn't intending to put them on a (distant) wall. The type I bought were for indoor use anyway. They came in at £16(ish) each and measure 320x160mm. They have fixing screw positions so you should be able to align these accurately when making bigger displays. Read hzellers Github page regarding daisy chaining to make bigger panels.


Power supply - I bought a 30A 5V Letour from Amazon - you need about 3A per panel when fully lit with white - though that would be a rare thing to do. I added some 3300uf caps to the panels supply to buffer against switching glitches. (Someone, on the net, more knowledgeable than me showed the calculations for that.) For use in a Truck/Lorry I would use one buck convertor per panel but for development I used the Letour. The Bucks will handle upto 3A and worked well in my prototype. Plus, you can feed in anything between 6v and 36v and get the 5v to drive the Pi and panels. I normally add a large value capacitor to the output for additional smoothing (belt and braces approach - may not be essential) If using multiple bucks make sure you common all the ground lines.

The link to the hzeller Pi active interface and software driver library is here:- https://github.com/hzeller/rpi-rgb-led-matrix

## LED Chains

The chain animation code uses the concept of chains of LEDs - basically just a list of XY co-ordinates for each LED. So, you can create you own lists or use the methods in Chain.py to create lines, rectangles and circles.

In python a chain is managed as two lists: the first is the XY list which never changes (The LEDs never move). The second is a list of colour objects which are used to store the current colour of the LEDs - this isn't needed by all animations but it allows rapid shifting by slicing the chain (Comet and Larson are examples) or manipulating the individual pixel luminance values (such as the Fade animations). Such animations then refresh the canvas to show the colours in their new positions.

### _makeRect(posX,posY,w,h,fillMode=None)_
Creates a rectangle at posX/posY of given width and height - units are 'pixels'.
If fillmode="H" the rectangle is constructed using horizontal lines of LEDs. Hence animations will run top left to top right and work their way down the rectangle. If fillmode is "V" the rectangle is vertically filled top to bottom, left to right.

### _makeCircle(cx,cy,r)_
This creates a circle with a radious of r pixels centred at cx/cy. The circle runs clockwise from the 9 o'clock position.

### _makeDisc(cx,cy,r)_
This creates a filled circle using smaller and smaller circles. It calls makeCircle to do the dirty work.

### _Custom chains_ 

These can be created and are just python lists of x/y tuples e,g [(x0,y0),(x1,y1),....(xn,yn)]. To do this you can use Inkscape to mark your LEDs on an image the process the SVG image using a python script. The script I wrote is available in the Chain Maker folder.


## The Animations

The animator code cycles through a list of animations using a palette of colours. The duration and speed of the animations can be set.

Unless otherwise stated, if the palette contains more than one colour they are cycled in the animation. Some animations may just use the first two colours or , if there's only one colour, use black as the second colour.

The code supports chain animations and text animations. Chain animations can be found in Animations.py, text animations can be found in TextAnimations.py and image animations in, well, ImageAnimations.py.

Parameters are passed to the animation using kwargs which are parsed when the animation class is instantiated - this provides a flexible framework to enable each animation to have it's own set of parameters.

Chain animations use the following parameters: duration,speed,palette and fps. Some animations may need to know their FPS in order to determine where they are in a cycle.


### Chain Animations  

#### FadeIn  
Selects the first palette colour then fades the LED chain in. Moves on to the next palette colour.

#### FadeOut  
Selects the first palette colour , sets the LEDs to full brightness then fades it out. Moves on to the next palette colour.

#### FadeInOut  
Selects the first palette colour then fades it in and out. Moves on to the next palette colour.

#### CometRight,CometLeft  
Creates a comet with a bright head and fading tail (5 leds long) then moves the comet. Starts over till duration has been exceeded. If a palette with more than one colour is provided the comet sections are coloured using the palette. It is difficult to visually discern brightness steps more than 5 (20% drop each time) - or it could just be my failing eyesight that's to blame.

#### CometsRight,CometsLeft  
Creates comets nose to tail then moves the comets. Starts over till duration has been exceeded. If a palette with more than one colour is provided the comet sections are coloured using the palette.

#### Sparkle  
Randomly selects colours from the supplied palette and truns on random LEDs within them.

#### SparkleRandom  
Uses a randomly created colour - ignores any palette.

#### AltOnOff  
Uses the first two colours from a palette and turns on alternate LEDs. If only one colour is in the palette black is used.
At each step the colours are shifted one place right - this, sort of,gives the illusion of them alternating like a pair of train crossing lights.

#### Pulse  
Selects the first colour from the palette. Uses speed as a Duty cycle value to turn LEDs on then off. So speed=0.25 means the LEDs will be on for 25% of fps. This is not intended for PWM control of brightness - that is done using the HSL luminosity value.
#### On  
Simply turns the LEDs ON or, if the colour is black, OFF.

#### Larson or KnightRider  
If you are old enough to know the Knight Rider TV series this is the light show on the front of the car (KIT). Google Larson Scanner for more info.

####Collider  
The leds are turned on at both ends of a chain and make their way to the centre where they collide in a blinding white flash which fades to black.

#### WipeRight,WipeLeft
The LED chain is filled from left or right.

#### WipeIn,WipeOut  
The LED chain is filled from both ends to centre or from centre to both ends.

#### Wait  
Does absolutely nothing till the duration expires - could be useful for synchronising the animations on two seperate chains. The current state of the LEDs in the chain are unchanged during the wait.


## Defining Animation Sequences  
Here's an example :-

Seq1=AnimSequence.AnimSequence([
    Animations.CometRight(duration=5,speed=1.0,palette=Palette.XMAS,fps=FPS),
    Animations.FadeInOut(duration=3, speed=0.1, palette=Palette.LOTS,fps=FPS),
    Animations.Larson(duration=10,speed=1,palette=Palette.RGB,fps=FPS)  
])

This defines Seq1 as three sequential animations. 

The first (CometRight) runs for 5 seconds at 1.0 speed using the XMAS palette found in Palette.py. 
This is followed by a FadeInOut animation for 3 seconds at one tenth speed then a Larson scanner animation lasting 10 seconds at full speed (1.0). This cycle will then repeat forever.

You would usually define one sequence for each chain of LEDs but you can use the same sequence on more than one chain at once.

### Animation Speed and Duration

The duration parameter is the number of seconds an animation should run for. The animation will abruptly stop at the end of this time period so if you care about a complete cycle you need to adjust the duration to match a whole number of cycles. That is down to you to work out.

The speed parameter is related to the frames per second (fps) of the animation system. All animations run at the same fps therefore your animation's step() method will always be called fps times per second (assuming all animation's step() methods complete in less than 1/fps seconds). 

The speed factor controls how many 'virtual ticks' are reported to your animation code. At a speed of 0.5 the virtual ticks will increment at half the fps, at 2.0 they will increment twice as fast. This can make your animations step through faster or slower.

If the speed factor is too low it can stall the animations. For that reason the code will add 10% to ensure your code receives the ticks.


## The Animation List

See main.py or the Truck logo example DAF.py:

Define your animation sequences first then create an instance of the Animator like this:-

`A=AnimLib.Animator(rows=PANEL_ROWS,chain_len=PANEL_SERIES,parallel=PANEL_PARALLEL,LEDspacing=5,LEDsize=5,fps=FPS)  `

The rows,chain_len and parallel parameters are passed to the RGBMatrix driver created by hzeller (https://github.com/hzeller/rpi-rgb-led-matrix). They are also used to calculate the dimensions of the RGB panel when using the simulator (TkInter window). LEDsize and LEDspacing are used by the simulator. The LEDs on my panels were spaced at 5mm but the actual LED size was smaller at 2mm. In practise, for simulation purposes I use 5 for both dimensions. I wouldn't try making the LEDsize bigger than the spacing as that would just make the LEDs overlap.
 
Next you add your animations like this:-

`A.addAnimation(chain=Chain(makeLine(0,4,64,4)),seq=Seq1)`

Animations are executed in the order given so the first is, effectively, the bottom layer. This can be an important consideration if your LED chains overlap.


