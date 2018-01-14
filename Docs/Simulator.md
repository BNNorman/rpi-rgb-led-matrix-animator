# Simulator

Whilst developing this code I decided to write a software simulator which could run on my desktop computer so that I 
didn't have to keep transferring the, rapidly, changing files to my Pi whilst debugging.

Initially I wrote the simulator using TkInter but found it too slow. A panel of 64x64 LEDs required 4096 items to be 
refreshed. Also, images and text didn't look like they would on a panel. So, I re-wrote the simulator using **openCV's 
imshow ()** and used **numpy** images with the same resolution as the target LED panel. 

The final output is scaled up for on-screen display. Afterall, a 64x64 bit image wouldn't view very well on a 1920x1080 
resolution screen now, would it?

The simulator code is in the Simulator folder it is included by the Panel.py script if the code is running on a 
Windows desktop.

If the animator code is running on a Pi the simulator is ignored and output goes direct to the RGB LED panel via the 
hzeller drivers downloaded from GitHub.

Of course, if you overburden the simulator your animation timings will suffer. Keep it simple, don't bombard your 
audience with too much going on.

## Parameters

Parameters are passed in as kwargs from the main script when the Panel is created like this :-
    
`Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS, 
               debug=True, videoCapture=True, videoName="./ImageDemo {width}x{height}.avi")`
               
My HUB75 panel is made of two 32x64 main panels stacked one on top of the other making a 64x64 array. Each main panel
 is constructed of two 32x32 sub-panels. Hence the paramaters are

**_for the panel:-_**  

**rows**        is the number rows in each panel (32 in my case but can be 16)  
**chain_len**   is the number of sub-panels in a main panel (2 in my case)  
**parallel**    is the number of main panels stacked on top of each other (2 in my case)  

**_For the simulator :-_**

**scale** is an overall screen-size multiplier (default is 2, increase to make the on-screen display bigger)

**_video recording:-_**

Like to show off your animations? (It can slowdown the screen refresh rate)

**videoCapture** if True video capturing takes place and records to an avi format file
**videoName**    default is "HUB75 {width}x{height}.avi" where **{width}** and **{height}** are the number of LEDs. You 
can also use **{screenWidth}** and **{screenHeight}** in the name
 the name begins with **./** the video appears in the same folder as the main script.
 
 _**Others:-_**  
 
 **fps** frames per second for the animation. Intended to tell the simulator how quickly to refresh the display but now 
 not used. Instead the RGBMatrix refreshes once per millisecond.  
 **debug** allows you to add debugging output from the Panel and RGBMatrix simulator.