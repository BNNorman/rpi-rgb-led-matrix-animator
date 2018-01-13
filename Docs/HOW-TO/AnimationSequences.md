#Animation Sequences

The animator code runs sequences of animations and is able to run several sequences at once. In fact one of the Chain
 demos runs 11 sequences using chains at the same time.
 
Each sequence can have multiple stages as in the following example. You would declare your sequences in your main.py 
script something like this :-

    Speed=1
    FPS=100
 
    SEQ1= AnimSequence.AnimSequence([
        ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
        ChainAnimations.FadeIn(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),
        ChainAnimations.Wait(duration=6, speed=Speed, palette=Palette.RED, fps=FPS),
        ChainAnimations.WipeRight(duration= 10, speed=Speed, palette=Palette.RGB, fps=FPS)
    ])

A sequence may include any or all animation types (sub-classes) and is not limited to ChainAnimations as in the example.

Each stage declares parameters for the animation:-

    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS),

The parameters **duration**, **speed** and **fps** are compulsory. However, image animations,for example, do not use a 
colour palette. In short - you must know what parameters your animations expect to use.

If you want the stage to loop until **duration** has expired you can add **animLoops=True** to the list.

When you write your own animations you can invent your own parameters like this:-

    class MyAnim(ChainAnimBase):
    
        param1=None
        param2="some texct"
        param3=1.56
        
**CAVEAT - don't duplicate parameters already used by the super classes ChainAnimBase and AnimBase.**

Within the stage you set the run time values of your parameters like this :-

    ChainAnimations.Collider(duration=5, speed=Speed, palette=Palette.RGB, fps=FPS, param1=55, param2="hello world", 
    param3=22),


