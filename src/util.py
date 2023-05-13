# util.py
# Lodinu Kalugalage
#
# Description: This file contains the utility functions used throughout the program.


# takes in lists, and joins them
# Example:
# A = [1, 2, 3]
# B = [4, 5, 6]
# C = [7, 8, 9]
# ripJoin(A, B, C) = [1, 4, 7, 2, 5, 8, 3, 6, 9]
def ripJoin(*args):
    return [item for sublist in zip(*args) for item in sublist]
