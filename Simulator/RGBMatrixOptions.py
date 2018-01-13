"""
RGBMatrixOptions.py

This is simply a collection of default options for the simulator.
The real Hzeller RGBOptions

"""

class RGBMatrixOptions(object):
    rows = 32
    parallel = 2
    chain_len = 2
    gpio_slowdown = 2       # gets rid of flickering leds on my Pi3
    drop_privileges = False # allow images to be loaded

    # a 64x64pixel display on screen is very small so we scale it up
    scale = 10

    # video capture
    videoCapture=False
    videoName="./HUB75 {width}x{height}.avi"

    # misc
    debug=False
    fps=100

    def validate(self):
        assert type(self.parallel) is int, "parallel parameter should be an int."
        assert type(self.rows) is int, "rows parameter should be an int."
        assert type(self.chain_len) is int, "chain_len parameter should be an int."
        assert type(self.gpio_slowdown) is int, "gpio_slowdown parameter should be an int."
        assert type(self.drop_privileges) is bool, "drop_privileges parameter should be a boolean."
        assert type(self.scale) is int, "scale parameter should be an int."
        assert type(self.videoCapture) is bool, "videoCapture parameter should be a boolean."
        assert type(self.videoName) is str, "videoName parameter should be a string."
        assert type(self.fps) is int, "fps parameter should be an int."
        assert type(self.debug) is bool, "debug parameter should be a boolean"