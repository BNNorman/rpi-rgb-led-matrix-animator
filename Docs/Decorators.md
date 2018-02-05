# Decorators.py

This script defines some decorators, from stackoverflow.com, for debugging class methods.

There's a whopping explanation of decorators [here](
https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators/1594484#1594484
).

## benchmark

This decorator is meant to be used within a class as it uses arg[0] to print the class name of the decorated method.

Placed in from of the step() method like this:-

    @benchmark
    def step(self):

results in this form of output :-

    Animations have been created
    Running
    Collider step() ran for 0.002614s
    FadeIn step() ran for 0.001606s
    WipeRight step() ran for 0.015923s
    WipeLeft step() ran for 0.001808s
    WipeIn step() ran for 0.001573s
    WipeOut step() ran for 0.001563s
    CometRight step() ran for 0.001580s
    CometsLeft step() ran for 0.001513s
    Larson step() ran for 0.001513s
    Sparkle step() ran for 0.002107s
    SparkleRandom step() ran for 0.001704s
    Pulse step() ran for 0.001538s
    AltOnOff step() ran for 0.001546s
    Pulse step() ran for 0.001967s
    Pulse step() ran for 0.001817s
    Pulse step() ran for 0.001653s

This shows how long each call took - all longer than the ambitious 100 fps (which is 0.01s).
 Ideally, they need to run 10x faster at least. So every animation type needs optimising in some way.
 
The first animation here is the Collider so the next frame begins with Collider again.