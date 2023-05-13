# util.py
# Lodinu Kalugalage
#
# Description: This file contains the utility functions used throughout the program.

# Dependencies on matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as pltpatches


def getColourAtIndexOrDefault(colours, index, default):
    if colours is not list:
        return colours
    if len(colours) > index:
        return colours[index]
    else:
        return default


def getSingularColour(colour):
    if type(colour) == str:
        return colour
    else:
        return getColourAtIndexOrDefault(colour, 0, "white")
