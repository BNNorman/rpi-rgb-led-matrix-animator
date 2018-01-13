#Text Animations

The software supports both openCV fonts and BDF fonts and differentiates between them by using the font name.

To use BDF fonts specify **fontName="BDF"** otherwise use **fontFace=FONT_HERSHEY_SIMPLEX** to use openCV fonts. The 
choice for rendering is made by **AnimBase.drawText()** which uses the current values of **self.fontFace**, **self.fontSize**
 etc.

The available fonts are listed in Constants.py.

Text can have transparency so you can place text over a background image. Background and foreground colors can be set
 as required by rendering the text into a buffer image then placing that.

##BDF Fonts

These are monospaced open source fonts without anti-aliasing. The fonts are listed in a dictionary (**BDF_FONT**) keyed by font size. 
Not all sizes are available they range from 6pt to 20pt but 11,16,17, and 19 are missing. The dictionary  
substitutes what I think will be a close fit. If you find similar BDF fonts for the missing sizes just edit the dictionary in 
Constants.py and add your font to the Fonts folder.

One advantage of the BDF fonts over openCV fonts is that you can colour each letter of a word differently using all 
the colours of the supplied palette.

A disadvantage is that the letters (currently) cannot be anti-aliased.

##OpenCV fonts

These are the Hershey fonts. They can be scaled to any size and can use anti-aliasing by using **lineType=LINE_AA**. 
Other line types are listed in Constants.py

At the moment, Hershey text cannot have different coloured letters - though you could create your own message from 
single characters with different colours. (tedious) I plan to add a Char class to treat a text message
 as seperate characters in a similar waty to how Chains work.

##Text Animation Sequences

The following is an example of a text animation sequence. The Move animation requires a start position and an end 
position.

    
    Seq= AnimSequence.AnimSequence([
        TextAnimations.Move(duration=5, speed=0.2, palette=Palette.RGB, fps=FPS, text="Float", 
        fontName=FONT_HERSEY_SIMPLEX, fontSize=16, startPos=(0,63), endPos=(0,0) ),  
        
        TextAnimations.Move(duration=5, speed=0.2, palette=Palette.CMY, fps=FPS, text="Sink",  
        fontName=FONT_HERSHEY_COMPLEX,
        fontSize=16, startPos=(0,0), endPos=(0,63)),  
        
        TextAnimations.FadeIn(duration=5, speed=0.2, palette=Palette.XMAS, fps=FPS, text="Scroll right", 
        fontName="BDF", fontSize=16, Xpos=0, Ypos=12),  
    ])

##Text length

Sometimes you want your text message to scroll right off the panel so you need to know how long it is. To do that you
 can call the **getTextSize()** function in UtilLib.py. In the example the first stage has been given a terminal 
 height of **-tHeight** which means it should disappear off the top of the panel since the default origin of the text is 
 top left. You can change that when drawing text using the parameter **bottomLeftOrigin=True**
 
     from UtilLib import *
     tWidth,tHeight=getTextSize("BDF",16,"my message")
     
     
     Seq= AnimSequence.AnimSequence([
            TextAnimations.Move(duration=5, speed=0.2, palette=Palette.RGB, fps=FPS, text="Float", 
            fontName=FONT_HERSEY_SIMPLEX, fontSize=16, startPos=(0,63), endPos=(0,-tHeight) ),  
            
            TextAnimations.Move(duration=5, speed=0.2, palette=Palette.CMY, fps=FPS, text="Sink",  
            fontName=FONT_HERSHEY_COMPLEX,
            fontSize=16, startPos=(0,0), endPos=(0,63)),  
            
            TextAnimations.FadeIn(duration=5, speed=0.2, palette=Palette.XMAS, fps=FPS, text="Scroll right", 
            fontName="BDF", fontSize=16, Xpos=0, Ypos=12),  
        ])

 
 
 
 
 
 def getTextLength(font,size,text,thickness=1):