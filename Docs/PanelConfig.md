# Panel Config

This document is no substitute for the excellent [README](https://github.com/hzeller/rpi-rgb-led-matrix) written by 
HZeller.

I'm going to explain my configuration in the hope it helps you with yours.

# Initialising the panel

You'll see this code near the beginning of my Examples :-

    PANEL_PARALLEL=2    # 2 in parallel = 64 leds vertical
    PANEL_ROWS=32       # each sub panel is 32 LED x 32
    PANEL_SERIES=2      # 2 in series = 64 leds horizontcal
    
    Panel.init(rows=PANEL_ROWS, chain_length=PANEL_SERIES, parallel=PANEL_PARALLEL, fps=FPS,
               debug=DEBUG,videoCapture=False,videoName="./TextDemo.avi")

As the comments say, my panels are 32x64 1:16 scan constructed, by the manufacturer, from two 32x32 subpanels - you can 
just see the join.

So, PANEL_ROWS is 32 and PANEL_SERIES is 2.

I have stacked two of these panels on top of each other so PANEL_PARALLEL=2.

I also added a 3300uf electrolytic capacitor across the panel supply **at the connector on the panel** this helps the
 PSU cope with surges from rapid switching. The calculations are shown at the bottom of the [wiring](https://github
 .com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md) document on 
 HZeller's site. If your panels have half as many LEDs you can halve the value but it's not worth the money saved.

There are a lot of other options as listed below. If added to the Panel.init() parameters they will be passed 
straight through to the HZeller RGBMatrix drivers - they are ignored by the simulator.

I used some display board from an office supplies shop to mount my panels (Screws from the back). A hot glue gun was 
used to make the display board stand up by gluing on a base and side supports.

# What does HUB75 scan 1/4, 1/8,1/16 etc mean? 

The HUB75 connector has two RGB channels so the panels are addressed top half and bottom half simultaenously. On a 32 
row panel like mine (1:16 scan) it means that the electronics will be driving row 1 and row 16 together. This reduces the 
address lines needed by 1 but the controller is clocking the data into the panel two pixels at a time.

You do need to know the internal construction of your panels - escpecially if they are made of much smaller 
sub-panels. I believe some zig-zag (Top L-R bottom L-R) and others are a U (across the 
top L-R and back along the bottom R-L).

I was fortunate - my panels are simple.

# RGBMatrix options

You can add any of the following options to the list of arguments in **Panel.init()**. They are passed straight through 
to the HZeller **RGBMatrix()**.

Most are left as the default. I think this list is correct.

    pwm_bits
    brightness
    hardware_mapping
    rows
    cols
    multiplexing
    row_address_type
    chain_length
    parallel
    pwm_lsb_nanoseconds
    scan_mode
    disable_hardware_pulsing
    show_refresh_rate
    inverse_colours
    led_rgb_sequence
    gpio_slowdown
    daemon
    drop_privileges
    luminance_correct

I'm not going to explain them here because that would meaan keeping up with HZeller's documentation.

The defaults I used are in **Panel.py** (see below) since I'm not likely to be changing the panel any day soon.

    ##########################################################################################
    # define the default options for a 64x64 matrix comprising of two 64x32 panels in parallel
    # each panel has two 32x32 sub-panels chained together
    # these are passed in via init(rows=x, ...)
    ##########################################################################################
    Options = RGBMatrixOptions()
    Options.rows = 32           # 32 rows in each panel
    Options.parallel = 2        # two panels in parallel
    Options.chain_length = 2       # sub-panels per panel
    Options.gpio_slowdown = 2   # gets rid of flickering leds on my Pi3
    
    # on Linux not doing this prevents access to images (files)
    # after the RGBMatrix is created
    Options.drop_privileges = False

