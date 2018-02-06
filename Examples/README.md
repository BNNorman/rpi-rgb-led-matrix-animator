# Examples

This folder contains some examples and video recordings of those examples.

They all import PathSetter.py first which makes sure that the parent folder is on the python sys.path so that the 
examples can import the LEDAnimator library bits and pieces.

# Running the examples on Windows

On the command line simply:-

    python <example>

From within, say,PyCharm just open the example and use the menu option Run or right click the window tab and select Run.


# Running the Examples on a Pi

This is similar to windows but you need to use an elevated command:-

    sudo python <example>

# drop_privileges

The animator does not enable drop_privileges when the RGBMatrix object is created. If drop_privileges is True it 
prevents your code from loading image files. 

Now, this is frowned on but I reckon if you are not networked it doesn't matter. 

If anyone can find a way to access image files with drop_privileges set True I'd like to hear it. (getpid/setpid etc didn't work for me, but I 
didn't spend a lot of time on it)

