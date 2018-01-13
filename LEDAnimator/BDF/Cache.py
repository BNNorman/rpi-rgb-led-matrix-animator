'''
FontCache.py

cachesrequests to load fonts to save time

'''

import LEDAnimator.BDF.Parser as Parser

#dictionary for the loaded fonts
glyphCache={}


def loadFont(path):
    """
    :param path:
    :return Glyph: the Glyph object
    """
    if path in glyphCache:
        return glyphCache[path]

    # parse the font file and store it in the cache
    glyphCache[path]=Parser.Parser(path)
    return glyphCache[path]


