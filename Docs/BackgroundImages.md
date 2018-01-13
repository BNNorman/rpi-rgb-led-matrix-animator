#Background Images

All animations can have background images but you also need to be aware of the layering that takes place

The following shows a collection of 9 animation sequences being added to the animator :-

    background=AnimSequence(...)
    DAF_D_SEQ=AnimSequence(...) # the other sequences would also be created in a similar way

    A=Animator(...)

    # add the sequences
    A.addAnimation(seq=background)  # bg images should be laid down first
    A.addAnimation(chain=Chain(DAF_D),seq=DAF_D_SEQ)
    A.addAnimation(chain=Chain(DAF_A),seq=DAF_A_SEQ)
    A.addAnimation(chain=Chain(DAF_F),seq=DAF_F_SEQ)
    A.addAnimation(chain=Chain(DAF_LEFTWING),seq=DAF_LEFTWING_SEQ)
    A.addAnimation(chain=Chain(DAF_RIGHTWING),seq=DAF_RIGHTWING_SEQ)
    A.addAnimation(chain=Chain(DAF_CROSS),seq=DAF_CROSS_SEQ)
    A.addAnimation(chain=Chain(DAF_OUTERCIRCLE),seq=DAF_OUTERRING_SEQ)
    A.addAnimation(chain=Chain(DAF_INNERCIRCLE),seq=DAF_INNERRING_SEQ)
    
They are rendered to the output buffer in the order added. Consequently the first sequence is the background and if 
you add a background image to a later sequence it could overwrite the earlier.

Foreground and background images can be added to animation sequences. Background images are always rendered but only 
Image Animations use foreground images.

The parameters for a background image are added to a dictionary object and passed into the animation sequence like 
this:-

    # declare parameters for the background image
    backdrop=Image(imagePath="../images/DAF_640_640.png",scaleMode="F",alignMode=("C","C"))
    
    # declare the animation sequence
    background= AnimSequence.AnimSequence([
        ImageAnimations.Wait(duration=10, speed=0.1, fps=FPS, bgImage=backdrop)
    ])`


The above just displays the background image. Since the image is not changes the **duration**, **speed** and **fps** are really 
irrelevant as there are no other stages in the sequence. 

NOTE: **scaleMode="F"** asks for the image to be scaled to Fit the panel. **alignMode=("C","C")** asks for it to be
centered both horizontally and vertically.
