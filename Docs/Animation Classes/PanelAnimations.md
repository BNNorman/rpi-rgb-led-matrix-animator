# Panel Animations

This class is intended to draw shapes in windows or on the whole panel.

Regular shapes like rectangles, circles and ellipses are drawn using the openCV drawing functions which allows you to
 use the LINE_AA (anti-aliased) or LINE_8/LINE_4 line types.
 
## RandomRectangles

The code generates coloured rectangles randomly using the palette of colors you specify

## RandomCircles

Similar to RandomRectangles

## RandomEllipses

Similar again

## RandomSparkle

The panel is filled with random colors which change

## Line

Draws a line

## PolyLines

Draws a sequence of joined lines from an XY coordinate list [(x0,y0)...(xn,yn)]. You could use a Chain for this.

If you set the animation parameter **multiColored=True** then each segment is drawn using the next color from the 
supplied Palette.

## Rainbow

Cyclically uses the colors from the supplied palette to draw vertical bands of specified width. You can achieve the 
effect of a moving vertical band if you adjust your band width and the length of the palette. (I haven't tried this 
but I think my PanelDemo program might do this.

## Twinkle

Uses a Poisson Disc random distribution to create a pleasing field of LED which are twinkled like stars in the sky, 
except with more color. 

## Wait

Does nothing - possible use would be to sync with another animation sequence.
 
