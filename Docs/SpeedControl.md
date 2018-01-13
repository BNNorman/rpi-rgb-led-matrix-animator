#Speed Control

When you set the animation fps to 100 the Animator **tries** to call the animation that number of times per second.

However, some animations may be time based - like a sine wave. So at speed=1.0 the animation should receive 100 ticks 
per second.
 
The system calculates which tick number the animation should see using the formula:-

`tick=int(speed*(time-start)*fps % fps)`  

So, if an animation runs longer than one second the tick value will wrap back to zero.

At full speed then this generates tick values of 0,1,2,3,4,5...fps-1  
At half speed it generates 0,0,1,1,2,2,3,3...fps-1  
At twice speed it produces 0,2,4,6,8,10,12,14,16,...fps-1  

So, for a sine calculation used in an animation, 

    y=math.sin(2*pi*(tick/fps))

should give the value of sin at the time of the tick.

To control the speed of your animation you need the following code at the very start of your step() method:-

    def step(self, chain=None):
        # speed control  
        if self.isNotNextStep():  
            self.refreshCanvas()
            return

Since the tick value is calculated from elapsed time from when the animation was reset and wraps every second the 
tick values should be correct, even if the animations are running a bit behind.