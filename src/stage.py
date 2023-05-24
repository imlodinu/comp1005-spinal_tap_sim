# stage.py
# Lodinu Kalugalage
#
# Description: This file contains the Stage related class which is used to represent
# the stage in the scene.

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  # Included with matplotlib

import constants as c
import colour as col
import util


class StageDescriptor:
    width = 0  # Width of the stage
    height = 0  # Height of the stage
    isFile = False
    backdrop = None  # Backdrop image (path to image prefixed with 'file://', colour, or None for no backdrop)
    source = None  # Storage for backdrop data

    # Constructor for a `StageDescriptor`
    def __init__(self, width=0, height=0, backdrop=None):
        self.width = width
        self.height = height
        self.backdrop = backdrop
        if isinstance(backdrop, str) and backdrop.startswith("file://"):
            self.addBackdropFromFile(backdrop[7:])

    # Adds a backdrop from a file
    def addBackdropFromFile(self, name: str):
        self.backdrop = "file://" + name
        self.isFile = True
        self.source = np.array(Image.open(util.getPath(name)))


def stageFromFile(name: str):
    # Uses PIL to open the image, then converts it to a numpy array
    return StageDescriptor(0, 0, np.array(Image.open(util.getPath(name))))


defaultStageCMAP = col.getOrMakeCMAP("black", "black")


class StageDraw:
    topAx: plt.Axes  # Top down axis
    sideAx: plt.Axes  # Side on axis
    descriptor: StageDescriptor  # Stage descriptor

    # Constructor for a `StageDraw`
    def __init__(self, descriptor):
        self.descriptor = descriptor

        fig = plt.figure(constrained_layout=True)
        gs = fig.add_gridspec(
            ncols=1,
            nrows=2,
            width_ratios=[1],
            height_ratios=[c.LIGHT_SOURCE_DIAMETER, descriptor.height],
        )

        self.topAx = fig.add_subplot(gs[0], facecolor="black")
        self.sideAx = fig.add_subplot(gs[1], facecolor="black")
        self.topAx.set_aspect("equal")
        self.sideAx.set_aspect("equal")

        # Done to keep the audience view the same
        _ = self.topAx.imshow(
            [[[0]]],
            cmap=defaultStageCMAP,
            extent=[0, descriptor.width, 0, c.LIGHT_SOURCE_DIAMETER],
            interpolation="nearest",
            alpha=1,
            origin="lower",
        ).set_zorder(-1)

    # Draws the stage's backdrop
    def draw(self):
        if self.descriptor.backdrop is None:
            return
        # Draws the backdrop
        if self.descriptor.isFile and self.descriptor.source is not None:
            self.sideAx.imshow(
                self.descriptor.source,
                extent=[0, self.descriptor.width, 0, self.descriptor.height],
                interpolation="nearest",
                alpha=1,
                origin="upper",
            )
            top = self.descriptor.source[
                0 : int(c.LIGHT_SOURCE_DIAMETER),
                0 : self.descriptor.source.shape[1],
            ]
            self.topAx.imshow(
                top,
                extent=[0, self.descriptor.width, 0, c.LIGHT_SOURCE_DIAMETER],
                interpolation="nearest",
                alpha=1,
                origin="upper",
            )
        else:
            cmap = col.getOrMakeCMAP(
                self.descriptor.backdrop,
                self.descriptor.backdrop,
                self.descriptor.backdrop,
            )
            self.sideAx.imshow(
                [[[0]]],
                cmap=cmap,
                extent=[0, self.descriptor.width, 0, self.descriptor.height],
                interpolation="nearest",
                alpha=1,
                origin="upper",
            ).set_zorder(-1)
            self.topAx.imshow(
                [[[0]]],
                cmap=cmap,
                extent=[0, self.descriptor.width, 0, c.LIGHT_SOURCE_DIAMETER],
                interpolation="nearest",
                alpha=1,
                origin="lower",
            )

    # Clears the stage
    def clean(self):
        self.topAx.patches.clear()
        self.topAx.images.clear()
        self.sideAx.patches.clear()
        self.sideAx.images.clear()
