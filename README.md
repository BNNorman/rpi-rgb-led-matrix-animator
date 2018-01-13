# rpi-rgb-led-matrix-animator
Python code to play animation sequences on an RGB LED matrix panel using the HZeller (https://github.com/hzeller/rpi-rgb-led-matrix) drivers on a Raspberry Pi (Model 3 used)

Inspired by the amazing ALA library for the Arduino.

## Currently supports:-

-multiple layers  
-animation sequencing (speed and duration control)  
-transparency  
-foreground and background images or colours    
-chain animations (like a LED strip folded)  
-text animations (like scrolling text messages)  
-image animations like fade in/out, dissolve, blur, blend,  hue change etc    
-panel animations like drawing randomly sized rectangles/ellipses etc  
-affine image transforms  
-image scaling with anti-aliasing  
-BDF and openCV fonts 

See the docs folder for more information

## Licence

Free to use and modify but credit me as the original author please. Please read License.md
 
This work took several months so, if you really feel grateful, you could send me money via my PayPal account - it would 
help my tiny pension.

## Requirements

Raspberry Pi
HZeller interface for the HUB75 panels (See OSH Park for pcbs for the active controller)  
The code is written for Python 2 and requires openCV, numpy, matplotlib, PIL (or pillow).

On the Raspberry Pi you need to install the HZeller drivers (https://github.com/hzeller/rpi-rgb-led-matrix)

## Getting Started

Try running the Exmaples then look at the code - I've tried to make it as flexible and intuitive as possible.

There will be some video demos on YouTube or you can look at Norman Truck Logos on Facebook to see the development of
 some of the animations.

## Apologies

I've tried my best to fully document this code. You'll find most documents in the Docs folder.

The Python scripts should all have doc strings.

If you find any omissions let me know.

If you improve the code - especially regarding execution speed - let me know.

## Color and Colour

Sorry guys, I'm English so colour is correct. However, I have tried to use color as that seems to be the adopted 
strategy. You may come across the word colour in places - it means the same as color LOL.