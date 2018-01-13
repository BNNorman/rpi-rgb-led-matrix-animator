#Utilities

Chain Maker and Text Chain Maker are a couple of programs I cobbled together to make chain creation easier.

##Chain Maker

This takes in an SVG document from Inkscape and generates a chain (a list of XY coordinates for a bunch of LEDs).

Step1: Place an image in the background using Inkscape  
Step2: Mark the positions of the leds using circles  
Step3: Save the file  
Step4: Edit the Chain Maker program to tell it which file to use.  
Step5: run the program  

The program will generate a python file containing the XY coordinate lists.

The program uses the Inkscape layers to name the seperate chains.

You can import the resulting file into your code.

##Text Chain Maker

Similar to Chain Maker but you feed it a text message and it does it's best to produce a chain which follows the text.



