# Debugging

Well, actually, tracing what is happening.

Most programmers, at some time, place statements in their code to find out where it is going.
 
The AnimBase object has two routines for this:-
- self._Debug(args)
- self._Warning(args)

_Debug actually calls _Warning but only if self.debug is true. So, by setting self.debug=False you can turn off 
debugging message. BUT, if you still want to make sure your message is output at all times use **self._Warning()** 
instead of **self._Debug()**.

Both methods pass their arguments to a print statement so you can pass parameters just as you would with print.

# Enabling debugging

First of all your main.py (or whatever you've called it) needs to turn off print statement buffering because that 
could result in messages getting inter-mingled. I do it this way:-

    import sys
    
    DEBUG=True
    
    if DEBUG:
        sys.stdout=sys.stderr
        
The use DEBUG in your code like **debug=DEBUG**. Then you can turn off all debugging and one place.

# id and debug parameters

**id** and **debug** can be set by your main.py code to your sequences etc as shown below:-
    
    DAF_D_SEQ= AnimSequence.AnimSequence([
        ChainAnimations.Collider(duration=5,id="DAF_D_Collider",debug=DEBUG, speed=Speed, palette=Palette.RGB, fps=FPS),
        ChainAnimations.FadeIn(duration=5, id="DAF_D_FadeIn",debug=DEBUG, speed=1, palette=Palette.RGB, fps=FPS),
        ChainAnimations.WipeRight(duration= 10,id="DAF_D_WipeRight", debug=DEBUG, speed=Speed, palette=Palette.RGB,
     fps=FPS)
    ])

Adding debugging output to the animator:-

    A= Animator.Animator(fps=FPS,debug=DEBUG)

There is no id as there's only one Animator object.

Adding **id** information to each animation
    
    A.addAnimation(chain=Chain(DAF_D),seq=DAF_D_SEQ,id="DAF_D_CHAIN_SEQ", debug=DEBUG)
    A.addAnimation(chain=Chain(DAF_A),seq=DAF_A_SEQ,id="DAF_A_CHAIN_SEQ", debug=DEBUG)
    A.addAnimation(chain=Chain(DAF_F),seq=DAF_F_SEQ,id="DAF_F_CHAIN_SEQ", debug=DEBUG)
 
With DEBUG set to True this is the sort of thing you might see :-
 
DAF_A_CHAIN_SEQ AnimBase.nextFrame() finishing after calling step() returning False Animation= Sparkle
DAF_D_CHAIN_SEQ AnimBase.refreshCanvas() finished. Animation= FadeIn
DAF_A_CHAIN_SEQ AnimBase.nextFrame() finishing after calling step() returning False Animation= Sparkle
DAF_D_CHAIN_SEQ AnimBase.refreshCanvas() finished. Animation= FadeIn
DAF_A_CHAIN_SEQ AnimBase.nextFrame() finishing after calling step() returning False Animation= Collider
DAF_D_CHAIN_SEQ AnimBase.refreshCanvas() finished. Animation= FadeIn
 
If you have not set an id you will see [No id] at the beginning of the messages.
 
 # Assert
 
 There are a number of assert statements throughout the code. These can be optimised out by compiling the code using 
 the -o flag.
 
 Alternatively, if your system test shows everthing is working as it should you could search for and remove the 
 asserts. After all, they were mainly put in for me, during debugging, to catch errant code.