# colour.py
# Lodinu Kalugalage
#
# Description: This file contains the Colour related class which is used to represent
# a colour in the scene.

# Dependencies
import matplotlib.colors as colors


class Colour:
    rawColour: str | list[str]  # Raw colour, can be a string, or a list of two strings

    # Constructor for a `Colour`
    def __init__(self, rawColour: str | list[str] = "white"):
        self.rawColour = rawColour

    # checks to see if it's a multiple colour colour
    def isGradient(self):
        return not isinstance(self.rawColour, str)

    # sometimes we only want one colour
    def getSingleColour(self):
        if self.isGradient():
            return self.rawColour[0]
        else:
            return self.rawColour

    # gets the colour at the index
    def getColourIndex(self, index):
        if self.isGradient():
            return self.rawColour[index]
        else:
            return self.rawColour


storedCmaps = {}


def getOrMakeCMAP(a, b, name=None):
    key = name if name else "light_" + a + "_" + b
    if key in storedCmaps:
        return storedCmaps[key]
    else:
        newCmap = colors.LinearSegmentedColormap.from_list(key, [a, b])
        storedCmaps[key] = newCmap
        return newCmap
