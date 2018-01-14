# AnimBase

The AnimBase class is the basis for all sub-classes of animation objects.

It is subclassed with ChainAnimBase, ImageAnimBase, TextAnimBase and PanelAnimBase which may, or may not, add to 
AnimBase but serve as a hook anyway for future changes.

AnimBase performs the following 


## reset()

This calls your reset() function after :-

- Resetting the startTime of the animation. 
- Setting init=True so your animation knows when it needs to reset.
- load any foreground/background images and scale/transform if required.

If an image's loadVisible flag is False it hides the image so you won't see a flash when the images is loaded then 
made invisible.

## setSpeed()

Your animation requests to run at a certain speed using the **speed** parameter. However, it has been noticed that is 
the speed is set too low the animations may stall. This routine tries to ensure that the minimum speed is 1/fps plus 10%


## loadImage()

Called during reset() to load your images. Not meant to be called from your animations.

Also scales/transforms images as required.


## nextFrame()

This does some pre and post processing before calling your aanimation's **step()** method.

Returns values are:-
- False if the animation hasn't finished, True if it has.

- checks if duration has been reached and returns False which causes the animator to move to the next animation.
- check if you have set the startPause parameter to non-zero and exits if so
- checks if you have set the endPause parameter and exits if so
- Works out the current tick value based on the **startTime** and fps.

If **speed=1.0** the tick value increases by one on each call to your animations's **step()** method

At a speed of 0.5 tick increases at half the fps rate 0,0,1,1,2,2,3,3,4,4,5,5 etc

At a speed of 2.0 tick increases at twice the fps rate 0,2,4,6,8 etc 

It records the lastTick value each time so that your animation can check if it should run.(see **isNotNextStep()**)


## animationHasFinished()

Meant to be called by your animation so that **endPaused()** works


## endPaused()

Returns True if the **endPause** duration has not expired and so can be used to freeze the animation briefly at the end.

## startPaused()

Returns True if the **startPause** duration has not expired and so can be used to freeze the animation briefly at the 
start.

## isNotNextStep()

Used by your animations to control it's speed. You should add the following code at the start of your animation's 
**step()** method.

    def step():
        if self.isNotNextStep():
            self.refreshCanvas()
            return

When the current tick value is calculated it yields a floating point number and is rounded down so that the tick 
value increments only as it goes to the next number by **nextFrame()** like this

        t=time.time()-self.startTime 
        ticks=t*self.fps 
        self.tick=int(self.speed*ticks) % self.fps

This method compares the last tick value to this one and if it hasn't increased returns True.


## drawChainOnLayerBuffer()

This is used internally to render any ChainAnimation onto the animation's layer buffer.

See **refreshCanvas()**

## getNextPaletteEntry()

If the animation has a palette parameter this will return the next Color (not color) and will wrap back to the start.

Your code can call and use this so :-

    color=self.getNextPaletteEntry().getPixelColor()
    
 Here color is an rgba image where rgb are ordered according to the RGB_B,RGB_G,RGB_B volues in Constants.py. 
 Basically, the simulator used BGR images but the actual RGB Panel is in RGB order.

## getRandomPaletteEntry

Similar to getNextPaletteEntry() but you can use this to, well, choose any one of the palette Colors randomly. 

## scaleImage()

Used internally to scale the image if you have included the **scaleMode** parameter in your foreground or background images.

The scaling used uses anti-aliasing and choose the best method for scaling up or down. Scaling is done using the 
original image. It is only called during **reset()** which means it is only called once. 

## refreshCanvas()

This causes all buffers to be written to the panel buffer and thence to the actual panel.

Rendering is done in this order:-
1 Background color
2 Background image (bgImage)
3 Foreground image (fgImage)
4 Chains
5 Text

The buffers are only rendered if they are not None.
