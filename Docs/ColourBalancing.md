# Colour Balancing

The Red,Green and Blue diodes in an RGB LED don't emit light equally brightly.

The Panel.py code adjusts the three channels when the final image is sent to the real LED Panel. This does not happen 
when the code is using the simulator since it is outputting to a Monitor screen and it looks ok to me.

To correctly balance my panel I had to use the following multipliers:-

    redAdjust=1.0
    greenAdjust=0.8
    blueAdjust=0.5
 
Notice that I set red to 1.0 (max) since red is the dimmest colour and I then adjusted the green and blue till I got 
white. Of course double check with pure red, green and blue, cyan, magenta and yellow. You might want to use a light 
meter to measure the intensity and fiddle till it's balanced.
 
The script **Constants.py** defines the brightness adjustment factors for each channel. Sorry, individual LEDs are 
not catered for. I'm not sure if the numpy arrays are fast enough and, anyway, my panels look fairly uniform to me.