"""
PanelCheck.py

This is a simple check, using HZellers simple square code, to make sure the
python rgbmatrix library can be accessed to drive the panel.

If this fails then check that you have installed rgbmatrix into

/usr/local/lib/python22.7/dist-packages

if not got to the python folder in the cloned HZeller folder and run:-

sudo make install

YOU WILL HAVE TO CHANGE THE PANEL OPTIONS TO SUIT YOURS

"""
from rgbmatrix import RGBMatrix,RGBMatrixOptions
import random

Options=RGBMatrixOptions()
Options.rows=32
Options.parallel=2
Options.chain_length=2
Options.gpio_slowdown=2
Options.drop_privileges=False

print "Panel size h=",Options.rows*Options.parallel," w=",Options.rows*Options.chain_length


matrix=RGBMatrix(options=Options)

canvas=matrix.CreateFrameCanvas()

while 1:

    for x in range(0, matrix.width):
        canvas.SetPixel(x, x, 255, 255, 255)
        canvas.SetPixel(canvas.height - 1 - x, x, 255, 0, 255)

    for x in range(0, canvas.width):
        canvas.SetPixel(x, 0, 255, 0, 0)
        canvas.SetPixel(x, canvas.height - 1, 255, 255, 0)

    for y in range(0, canvas.height):
        canvas.SetPixel(0, y, 0, 0, 255)
        canvas.SetPixel(canvas.width - 1, y, 0, 255, 0)

    canvas=matrix.SwapOnVSync(canvas)