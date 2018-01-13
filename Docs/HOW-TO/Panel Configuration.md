#Panel Configuration

To drive your RGB LED panel you need to tell the hzeller drivers what you have. My code uses this snippit to create a 
panel:-

```
PANEL_ROWS=32
PANEL_PARALLEL=2
PANEL_SERIES=2

Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS,
           debug=False, videoCapture=True, videoName="./ImageDemo {width}x{height}.avi")


My panels are arranged like this (sort of):-

```
 ->[32x32]->[32x32] (top chain)
 ->[32x32]->[32x32] (middle chain)
```

The -> indicates signal flow. I use the top and middle chains on the hzeller designed RpI Hub75 active interface board - nice job! You can buy the PCBs from OSH PARK at https://oshpark.com/shared_projects/fIYlJxnA. Don't bother with the passive board - the active board translates the Pi 3.3v to the panel 5v - far better if driving big panels.

Physically they are two 32x64 panels in parallel. Each panel is actually two 32x32 panels. So it is resally a 2x2 arrangement each with 32 rows hence the values I used.  LED_spacing and LED_size are used by my TkInter panel simulator.

Now, the hzeller drivers are quite flexible so I suggest you read his notes. The link to the hzeller Pi active interface and software driver library is here:- https://github.com/hzeller/rpi-rgb-led-matrix

If you need to tweak the driver options then you need to edit AnimLib.py - look at the code on line 106 and add your own extras.

##Panel Supplier
If you are looking for panels I got mine from AliExpress https://www.aliexpress.com/item/seamless-splicing-Led-Module-P5-32-64-Pixles-320-160mm-1-16-scan-indoor-rgb-full/32810362786.html for £16.03 each with free shipping. They came with a Y splitter power lead and HUB75 ribbon cables (16pin DIL).

##Power Supply

You will need a beefy 5V power supply. 

When all LEDS are full on the panel will be sucking 60mA per LED. According to the supplier, my 32x64 panels draw 20W maximum (each) so I needed at least a 40W PSU. I actually went much bigger in case I needed more on a future project. 

I also added 3300uf caps, across the power connectors on the panels, to smooth out any potential supply dips when all leds come on at the same time. 

With this arrangement, I am able to run a pre-scaled movie at 25fps using my Pi3 (no sound though, but then most advertising boards don't use sound and a lorry driver wouldn't want this blaring out behind him). This ensures I could also use the panel for a slide show with animated transitions, if I wanted to.