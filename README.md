# rpi-rgb-led-matrix-animator
Python code to play animation sequences on an RGB LED matrix panel using the HZeller (https://github.com/hzeller/rpi-rgb-led-matrix) drivers on a Raspberry Pi (Model 3 used)

Coming soon - currently working on documentation and more testing

##Currently supports:-

*multiple layers

*animation sequencing (speed and duration control)

*colour transparency
 
*foreground and background images 

*background colours

*chain animations (like a LED strip folded)

*affine image transforms 

*BDF and openCV fonts 

##Animation classes:-

*TextAnimations - colour changes, scaling/moving

*ImageAnimations - colour manipulation, shape transforms, dissolve, slide and Pan 

*ChainAnimations - a lits of LED coordinates which can be manipulated using animations such as collide, Knight Rider (Larson),Fade,Sparkle to name only a few 

