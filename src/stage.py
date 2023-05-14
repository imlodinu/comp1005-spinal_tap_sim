# stage.py
# Lodinu Kalugalage
#
# Description: This file contains the Stage related class which is used to represent
# the stage in the scene.

import matplotlib.pyplot as plt

import constants as c
import colour as col


class StageDescriptor:
    width = None  # Width of the stage
    height = None  # Height of the stage
    backdrop = None  # Backdrop image (path to image prefixed with 'file://', colour, or None for no backdrop)

    # Constructor for a `StageDescriptor`
    def __init__(self, width=0.0, height=0.0, backdrop=None):
        self.width = width
        self.height = height
        self.backdrop = backdrop


defaultStageCMAP = col.getOrMakeCMAP("black", "black")


class StageDraw:
    topAx = None  # Top down axis
    sideAx = None  # Side on axis
    descriptor = None  # Stage descriptor

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
            [[[0, 0, 0, 0]]],
            cmap=defaultStageCMAP,
            extent=[0, descriptor.width, 0, c.LIGHT_SOURCE_DIAMETER],
            interpolation="nearest",
            alpha=1,
            origin="lower",
        ).set_zorder(-1)
