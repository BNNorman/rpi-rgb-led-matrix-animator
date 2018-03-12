# TrueType, OpenType and PIL fonts

These fonts will be rendered using the PIL image library

# Anti-Aliasing

Fonts are rendered as anti-aliased by default. To render without specify the lineType paramater as anything other 
than LINE_AA (e.g. LINE_8 or LINE_4 - just foir uniformity with copenCV Hershey fonts)

WARNING: I have seen rubbish results caused by turning off anti-aliasing with at least one TTF font.

# PIL fonts

PIL fonts comprise of two files <name>.pil and <name>.pbm - the latter is a portable bitmap format (text) 
character bitmap.

# Text length and Kerning

PIL uses kerning to calculate the length of a rendered text string. However, this doesn't play nicely when rendering 
multi-colored text which results in characters missing from the end of a string as a result of each character being 
positioned according to it's width. 