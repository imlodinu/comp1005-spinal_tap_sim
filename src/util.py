# util.py
# Lodinu Kalugalage
#
# Description: This file contains the util functions used throughout the program.

import pathlib  # Included with python


# If the program is called from different directories, then the relative path will be different
# This function gets the absolute path of a file relative to this file
def getPath(name: str):
    return str((pathlib.Path(__file__).parent / name).absolute())
