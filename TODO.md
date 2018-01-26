# TODO List

No promises!

1. add CharAnimations - a text string in which each character can be separately animated like LEDs in a Chain. It would
 be 
clumsy to do as individual TextAnimations of 1 character length as it wouldn't be possible to accurately synchronise 
movement.
2. Amend the Text object to move the position variables (Xpos and Ypos) into the object to be consistent with the 
Image object
3. Find out why Chain animations run faster on my PC than on the Pi whilst Image animations still run like stink. 
Obviously the problem lies upstream of the code which sends the rendered chain off to the Panel.
I have improved the speed of the RGBMatrix.updateDisplay() routine but the simulator still struggles to get over 
30fps, which is acceptable for this style of animation.


4. Find a faster Poisson Disc routine for PanelAnimations.Twinkle class (DONE!)