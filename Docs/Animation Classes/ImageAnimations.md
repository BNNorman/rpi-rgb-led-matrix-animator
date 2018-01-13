
# Image Animations

This document just discusses the default image animation parameters

When an RGB image is first loaded it is cached in RGB format with the alpha channel (if any) removed. This is then converted to an HSV image, after applying any resizing. The HSV image is cached and used for cumulative transforms.

If a transform requires the image to be resized again the HSV is discarded and recreated at the desired size. The aim is to try to avoid doing image resizing during animation loops.

In order to maintain quality, if an image is resized the original image is used. This means that any other prior changes will be lost and need to be re-applied.

The default parameters that can be passed to all image animations are:-

***imagePath***
The path to the image file. Any image supported by openCV can be imported.

***fps***
The frame rate of the animation

***speed***
A floating point number representing the relative speed of the animation. 1.0 means the animation will receive a clock tick at the fps rate.

***duration***
How long to continue the animation for. If the animation cycle time is less than duration it will be repeated until the duration is reached. Likewise, if the animation cycle time is longer than duration the animation will terminate mid-cycle. Currently, this is a trial an error setting as it is influenced by how many animations are running at any given time.

***scaleMode***
This is a string which can be V(ertfit),H(orizfit),B(othfit). With V and H the aspect ratio of the image is maintained. With B the image may be stretched in one dimension.

***align***
This is a tuple (X,Y) of two letters denoting the required placement of the image relative to the canvas. X controls the horizontal placement using L(eft),R(ight),C(entre) or M(iddle). Y controls the vertical placement using T(op),B(ottom) and C(enter) or M(iddle). Only the first letter is used so you can spell Centre as Center.

***transMatrix***
This is a string of 6 numbers corresponding to the 2x3 affine transform matrix values. The first three values correspond to the first row of the matrix and the last three to the bottom row. In python this is just a list of two lists thus:-

```
matrix=  [[a,b,c],[d,e,f]]
```
        
If a transform requires scaling (a<>1 or e<>1) the original image is first scaled then any other transforms are applied. This means that any changes of HSV values etc need to be re-applied during the animation.
One circumstance this might happen is with a spinning rotation or changing shear. The reason for applying transforms to the original is to maintain the best quality for the scaled image.

Only the first 6 numbers will be used. Non-numeric values will cause the transform to be ignored.

***Xpos, Ypos*** the panel coordinates of the top left corner of the image. Not needed with some Animations such as PanAndZoom which use startPos and endPos tuples.
 
        
## Available (default) Image Animations
### Place
This animation just draws the image at the required location

### Wait  
Does nothing but wait for the specified duration. The led chain is left in the state which the previous animation left it.


### PanAndZoom
Scrolls the image whilst zooming in or out.

extra parameters: 

***startPos*** A tuple (x,y) - panel coords for start of the pan (top left corner of the image is placed here). On a 64x64 matrix 32,32 would be the middle.  
***endPos*** A tupel (x,y) - panel coords for the end of the pan position.  
***zoom*** A tuple (a,b) - where a is the initial scale factor and b is the end scaling factor.  
***imagePath*** Path relative to the code location.

### Fade,FadeIn,FadeOut

FadeIn and FadeOut are subclasses of Fade.

***fadeRate***
Determines if the Fade animation is a fade in (+ve) or fade out (-ve). This paraemeter together with speed determines how quickly the fading takes. 

### RevealIn and RevealOut

Exposes an image - I suppose this could also be called a wipe. The image is exposed or hidden as the reveal takes place.

### ExpandIn and ExpandOut

The image expands outwards from the centre. The image can be exposed or hidden

### CollapseIn and CollaspeOut

The image grows from the outer edge to the center. The image can be exposed or hidden

### TheMatrix

If you've seen the Matrix screen saver ...

### DissolveIn and Dissolve out

Ranmdom pixels are made visible or invisible till the image has fully appeared or disappeared.
