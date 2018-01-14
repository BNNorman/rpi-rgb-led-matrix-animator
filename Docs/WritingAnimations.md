# Writing Animations

This program supports a number of types (sub-classes) of animations:-

1. Chain Animations (ChainAnimations.py)
2. Text Animations (TextAnimations.py)
3. Image Animations (ImageAnimations.py)
4. PanelAnimations (PanelAnimations.py) 

They each work in basically the same way but are grouped for convenience. Panel animations are just a collection of 
visually pleasing graphics - the Panel is treated a bit like a drawing board - draw what you like on it.


You can add your own animation sub-classes if you want/need to.

## Creating an animation

The basic template is :-

    class animation_name ( base_class ):
        
        def step(self):
            # speed control
            if self.isNotNextStep():
                self.refreshCanvas()    # essential!
                return
                
            if init:
                # do your init stuff
                #
                #
                # make sure this code doesn't run on next tick
                self.init=False
                #
                # you may wish to 'return' here 
    
            # do your stuff here
            
            # finally
            self.refreshCanvas()
        
The method **step()** is called fps (frames per second) times per second, if possible. If you have a slow animation in 
your list it could be delayed.

When **step()** is called, the variable **self.tick** is set according to your animation speed. If your speed is 1.0 then
 it increments in steps of 1 from 0 to fps (0,1,2,3,4..) every second. If you set speed to 2 it increments in multiples of 2. i.e 0,2,4,6,8..fps
and at half speed you get 00112233445566. So, animations which are tick based can used the tick value to compute where they should be at.

The call to **self.isNotNextStep()** returns True if the current time elapsed is between ticks and is an attempt to 
control the animation speed. It is named so that it reads sensibly rather than having to write 'if not isNextStep()'.

Within the **step()** method you should check **self.init**. If true, execute your initialisation code and when 
finished set **self.init=False** otherwise you'll get false **reset()** calls before every call to **step()** which 
would mean your animation doesn't progress.

Look at the examples to see how I wrote the animations (I'm sure they could be optimised).

## Animation sub-classes
All animation types inherit from the AnimBase object which processes the parameters passed in for the animation. The sub-classes are, currently, ChainAnimBase, TextAnimBase and ImageAnimBase. These provide an opportunity to do something which is only related to the individual animation subclasses. At some stage you might want to add other types of animation sub-classes.  

## AnimBase

All animation types inherit from the AnimBase object which processes the parameters passed in for the animation. The sub-classes are, currently, ChainAnimBase, TextAnimBase and ImageAnimBase. These provide an opportunity to do something which is only related to the individual animation subclasses. At some stage you might want to add other types of animation sub-classes.  

First of all, the `__init__` function accepts all the keyword arguments, for the animation, and uses them to set the attributes of the animation object instance like this:-

    def __init__(self,**kwargs):
        # gather any passed in values
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

This is a very flexible way to pass any parameters without knowing what they are called beforehand. However, it is also very dangerous since it is possible to clobber variables used by AnimBase.
Perhaps, in a future release, animation parameters will be created on a private object to avoid collisions. For now, you need to know which parameters AnimBase uses to control the execution of your animations.

## Using Inheritance

It is possible you might want to create an animation which is sub-classed to behave in different ways. I'll use Fade as an example. You would want be able to fade in and fade out some LEDs.

To do that you would first cdreate your basic Fade object which uses a direction parameter to determine if it should fade in or out.

Here's the definition for the Fade object which, by default, fades in.

    class Fade(ChainAnimBase):
    
        direction=1 # default is fade in
        
        def __init__(self,**kwargs):
            super(Fade,self).__init__(**kwargs)

You could use this to fade in by writing :-
    
    ChainAnimations.Fade(duration=5,speed=1,palette=palette.XMAS, fps=100,direction=1)`

or, to fade out :-
    
    ChainAnimations.Fade(duration=5,speed=1,palette=palette.XMAS, fps=100,direction=-1)
Alternatively you could sub-class Fade as FadeIn and FadeOut so you could write this instead :-
    
    ChainAnimations.FadeIn(duration=5,speed=1,palette=palette.XMAS, fps=100)
    ChainAnimations.FadeOut(duration=5,speed=1,palette=palette.XMAS, fps=100)

This is how to sub-class Fade (which has already been done):-
      
           
    class FadeOut(Fade):
    
        direction=-1
    

    class FadeIn(Fade):
    
        direction=1

The direction parameters override the super class parameter.


## Animation Sequences

Here's an example animation sequence which you would put in your main.py script :-

    FPS=100
    Speed=1
    
    DAF_F_SEQ= AnimSequence.AnimSequence([
        ChainAnimations.Wait(duration=6, speed=Speed, palette=Palette.RED, fps=FPS),
        ChainAnimations.FadeIn(duration=3, speed=Speed, palette=Palette.RGB, fps=FPS),
        ChainAnimations.Wait(duration=3, speed=Speed, palette=Palette.RED, fps=FPS),
        ChainAnimations.WipeRight(duration=10, speed=Speed, palette=Palette.RGB, fps=FPS)
    ])

During animation execution, when the duration has expired for any stage, the animation forcibly moves to the next 
animation in the sequence.

At the start of each stage of the sequence the animation code calls the **reset()** method for the animation. The 
**reset()** method sets **self.init=True** to tell your code to start over. Within your **step()** method you should 
set **self.init=False** to allow the animation to progress (See the basic template above).

## Animation looping

By default, animations will play once and stop then wait until the set duration has expired before being reset.

Within your animation sequence you can set **animLoops=True** to cause tha animation to loop over and over 
till duration has expired.

Within your **step()** method, at a point where your animation has reached it's conclusion, you can do this-

    self.animationHasFinished()
    
If you include the parameter **animLoops=True** in your sequence the animation will be **reset()** otherwise it will 
hold it's current state till duration has expired.

# Pausing Animations

Animations can be paused before they start and when they have finished (but before the animation loop continues).

Remember:-

    duration=startPause+animation time+endPause

So if you set a **duration** of say 10 seconds, a **startPause** of 2 seconds and an **endPause** of 2 seconds that leaves 6 
seconds for the actual animation.


## pause before the animation starts

If you declare a parameter **startPause=nn** the animation images will load and the animation will pause for nn 
seconds before it begins.

This is to give people a chance to see the initial state of your animation before it starts.

## pause at the end of the animation

You would need to include **endPause=nn** as a parameter in your animation sequence. This will cause the 
animation to hold its final state for nn seconds.

To use the end pause capability you need to tell the code when your animation has finished. You do that with a call to 
  **self.animationHasFinished()** 


