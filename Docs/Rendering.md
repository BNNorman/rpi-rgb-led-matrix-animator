# Rendering

Animations are rendered to a layer buffer to enable the use of transparency.

Each animation layer is then added to the Panel buffer in the same order that animation sequences are added to the 
animator.

For example. In the textDemo.py file you will see these lines of code

    # create the animator object
    A= Animator(debug=True,fps=FPS)
    
    # add the sequences the order is bottom layer to top layer
    A.addAnimation(seq=textAnimsBdf)  # bg images must be laid down first
    A.addAnimation(seq=textAnimsCV2)

This adds two animations to the animator hence the first is the bottom layer and the last is the top layer.

If you want to use a background image and play these animations over it then the background image should be added to 
the first animation. See Docs\BackgroundImages.md

Within each layer the layer itself is rendered in this order:-

    background
        any plain colour can be used to prefill the panel 
    bgImage
        a background image is rendered next
    fgImage
        a foreground image is rendered next
    Chains
        next any chain animations are rendered
    Text
        finally text is rendered on the topmost layer

 Text can be made to disappear behind something if the text animation is on a layer below that something.
   