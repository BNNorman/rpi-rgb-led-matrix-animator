# Requirements

## software
The code was developed on a Windows 10 desktop computer using PyCharm and Anaconda2. I chose Anaconda2 because it had 
a number of the other dependencies already included.

The code uses the following python libraries:-

- numpy for fast array manipulation of images and lists
- matplotlib - fast array conversion of hsv to rgb (mostly chain animations)
- openCV - the simulator uses cv2.imshow() for display and video capture for publishing demos. It also uses openCV to
 load images for animations.
- threading - the simulator runs in it's own thread to try to keep the frame rate up.
- colorsys - for single pixel hsv to rgb conversion

## hardware

- Raspberry Pi. All testing was done using a Pi 3.
- HUB75 panels. I used two 64x32 HUB75 panels bought from AliExpress ( Shenzhen Lightall Optoelectronics Co., LTD) 
for about £16 each. I added 3300uf capacitors across the supply at each panel to help cope with switchiung surges.
- HZeller active interface boards non-active are not recommended. You can order 3 of the PCBs from OSHPark 
(https://oshpark.com/shared_projects/bFtff2GR)( - the price was very reasonable for 3 boards, free delivery and they 
keep you informed by email as the boards are being made.) - I recommend you go for the Active design as it level shifts the 3.3v Pi GPIO to the 5v required by the HUB75 panels. Make sure you buy the exact components specified - they work a treat. I got mine from Amazon/Ebay. Practise some SMD soldering before you build the boards.
- components - Ebay, not expensive - see HZeller's list
- 5V Power Supply - I bought a 30A fanless supply from Amazon - works just fine. 4096 LEds sucking 60ma each at full 
brightness is an awful lot of current - more than 30A actually, but my display works well and it isn't on full 
brightness all the time so I got away with it.

## SMD Soldering

Just a brief tip when soldering the bus tranceivers. Add solder to one pad (on the pcb) then anchor the component using 
that pad. Then drag solder the rest of the pins. 

You may need a solder sucker to remove bridges but the technique works.

