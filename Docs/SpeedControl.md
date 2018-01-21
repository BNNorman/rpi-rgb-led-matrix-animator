# Speed Control

When you set the animation fps to 100 the Animator **tries** to call your animation's **step()** method that number of 
times (ticks) per second. Overly long animation functions can delay the calls.

To try to prevent animations lagging you have to control where it has gotten to using either time or by counting 
ticks.

The **AnimBase** object computes the current tick number when **AnimBase.nextFrame()** is called and before your animation's 
 **step()** method is called. The calculation is based on the **speed** parameter set for your animation.

When checking animation timings using the Simulator it's a good idea to diasble videoCapture

## Tick based control
 
The **AnimBase.nextFrame()** calculates which tick number the animation should see using the formula:-

    self.tick=int(speed*(current_time-start_time)*fps % fps)  

So, at **speed=1.0** and **fps=100**, **self.tick** will normally increment by one each time. However, if, for some 
reason, an another animation delays the **Animator** loop it could increase erratically e.g. 0,1,3,4,7 etc but it 
will be the correct value for the elapsed time and speed.

So, assuming all your animations, in a given loop, all run in under 1/fps seconds the value of tick will increase as 
follows:-

At full speed then this generates tick values of 0,1,2,3,4,5...fps-1  
At half speed it generates 0,0,1,1,2,2,3,3...fps-1  
At twice speed it produces 0,2,4,6,8,10,12,14,16,...fps-1  

You animation should check if, for example, the current tick value has increased. It does that by calling 
**self.isNotNextStep()** which returns True if not. Your animation should then call **self.refreshCanvas()** and return 
immediately. That should enable you to control the animation speeds like this:-

    def step(self, chain=None):
        # speed control  
        if self.isNotNextStep():  
            self.refreshCanvas()
            return

So, for a sine calculation used in an animation, 

    y=math.sin(2*pi*(tick/fps))

should give the value of sin corresponding to the time of the tick.

## Time based control

Another way to control your animation is to calculate how long your animation has been running. 

For example, you might want to fade in your animations from zero to full on over the **duration** you set for the 
animation rather than repeat the animation over and over during the **duration**.

Every time an animation is reset **self.startTime** is also reset to the current time. So you can calculate the time 
elapsed using this formula.

    elapsed=time.time()-self.startTime

The actual time that an animation has available to run depends on wether or not you have set a **startPause** or 
**endPause** so the actual duration of the animation would be calculated like this :-

    availableTime=self.duration-self.startPause-self.endPause

Thus, if you specify a duration of 10 seconds, a **startPause** of 2 seconds and an **endPause** of 1 second the time 
available for the animation is 7 seconds.
    
For a sine based animation which cycles through 360 degrees (2Pi radians) in the available time you calculate the value 
using:-

    value=sine((elapsed/availableTime)*2*pi)    
    
You can then use value to calculate where you animation should be.