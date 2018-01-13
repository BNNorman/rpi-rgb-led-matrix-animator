#Simulator
Provides an on screen representation of an RGB LED matrix for testing/developing animations for the same.

Originally, I used TkInter to simulate a matrix because, well, it was easy to code but it proved to be too slow. With a 64x64 matrix there are potaentially 4096 canvas objects, each representing 1 LED, to update. This was taking 4 seconds or so, if the entire matrix was being updated. The background image, when used in image animations, was taking about 0.2 seconds to place. At low frame rates of 30fps there's only 0.33 seconds available to update the animations which meant there was a lot of flickering.

The majority of the problem was caused by scaling of the matrix for display. Internally, the animator software manages an image the same size of the target matrix but on a PC screen that would be too small.

To overcome the problem I decided to write my own simulator using openCV. I know OpenCV can achieve 30fps on a raspeberry Pi when displaying the frames from a video which has been prescaled to the same size of the target matrix.. 

When the simulator window is open pressing any key will close it and terminate the simulator

#Technical
##Matrix
This class represents the LED RGB matrix. It is double buffered so that calls to SwapCanvas() are required once per frame period.

##BdfFont
This class loads and BDF character font sets. Currently it only supports BDF fonts in which the first entry is a space and the following characters are in order of the ASCII encoding. The character bitmaps are stored in a list such that the data for a glyph can be extracted with simple list indexing.

##Font
This class caches the characters from a font set. To handle multiple fonts code should instantiate a seperate Font class for each.

When a font file is loaded it is cached. Characters are rendered as black/white HSL images to numpy arrays and cache on demand.

Current foreground and background colours are applied when the glyph is used.