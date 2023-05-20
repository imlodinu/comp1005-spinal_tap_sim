# prop.py
# Lodinu Kalugalage
#
# Description: This file contains the prop related classes

# dependencies
import numpy as np
from matplotlib import pyplot as plt
from skimage.transform import resize

# included with matplotlib
from PIL import Image

from typing import Tuple


class Prop:
    img: np.ndarray  # Image of the prop
    position: Tuple[float, float]  # Position of the prop
    scale: float  # Scale of the prop

    # Constructor for a `Prop`
    def __init__(self, img: np.ndarray, position: Tuple[float, float], scale: float):
        self.img = img
        self.position = position
        self.scale = scale

    # Draws the prop
    def draw(self, ax: plt.Axes):
        # https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.resize
        scaledimg = resize(
            self.img,
            (
                int(self.img.shape[0] * self.scale),
                int(self.img.shape[1] * self.scale),
            ),
            order=0,  # nearest neighbour
        )
        ax.imshow(
            scaledimg,
            extent=[
                self.position[0],
                self.position[0] + self.img.shape[1] * self.scale,
                self.position[1],
                self.position[1] + self.img.shape[0] * self.scale,
            ],
        )


def propFromFile(name: str):
    # Uses PIL to open the image, then converts it to a numpy array
    return Prop(np.array(Image.open(name)), (0, 0), 1.0)
