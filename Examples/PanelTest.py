"""
PanelTest.py

Just a test to see how quickly the panel can be cleared

"""
import LEDAnimator.Panel as Panel
import time

FPS=30 # frames per sec for the animation

# my panel is 64x64 made up of two panels stacked on top of each otherizontal
PANEL_PARALLEL=2    # 2 in parallel = 64 leds v
# each panel is a single piece but is made of two 32x32 panels side by side
PANEL_ROWS=32       # each sub panel is 32 LED x 32
PANEL_SERIES=2      # 2 in series = 64 leds horertical



Panel.init(rows=PANEL_ROWS, chain_len=PANEL_SERIES, parallel=PANEL_PARALLEL,LEDspacing=5, LEDsize=3, fps=FPS, debug=True)

t0=time.clock()

Panel.Clear((255,255,255))

t1=time.clock()

print "main() Panel clear took %.4f seconds. Average=%.6f per pixel" % (t1-t0,((t1-t0)/(64*64)))




