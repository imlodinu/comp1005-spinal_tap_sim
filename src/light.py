# light.py
# Lodinu Kalugalage
#
# Description: This file contains the Light related class which is used to represent
# a light source in the scene.

# Dependencies on matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as pltpatches

import stage
import colour as col
import constants as c
import util as u

import math


class Light:
    colour = None  # Colour
    position = None  # a 1D representation of the light's position, as it is fixed on the ceiling in a 2D
    direction = None  # 0-180, 0 is facing right, 90 is facing down, 180 is facing left
    intensity = None  # 0-11, 0 is off, 11 is brightest
    spread = None  # 0-120, cone of light spread, 0 is a laser, 120 is a flood light

    # Constructor for a `Light`
    def __init__(
        self, colour=col.Colour(), position=0.0, direction=90, intensity=5, spread=25
    ):
        self.colour = colour
        self.position = position
        self.direction = direction
        self.intensity = intensity
        self.spread = spread

    # Draws the light from a topdown perspective on the plt axes
    def drawTopDown(self, stageInfo: stage.StageDescriptor, ax: plt.Axes):
        # Position is from the middle of the stage
        middleOfStage = stageInfo.width / 2
        lightCirclePosition = [middleOfStage + self.position, c.LIGHT_SOURCE_RADIUS]
        lightCircleRadius = c.LIGHT_SOURCE_RADIUS
        # Colour can be a list of colours, or a singular colour
        lightColour = self.colour.getSingleColour()
        lightCircle = pltpatches.Circle(
            lightCirclePosition,
            lightCircleRadius,
            color=lightColour,
            alpha=self.intensity / 11,
        )
        ax.add_patch(lightCircle)

    # Draws the light from the audience's perspective on the plt axes
    def draw2D(self, stageInfo: stage.StageDescriptor, ax: plt.Axes):
        middleOfStage = stageInfo.width / 2
        LightConeBeamCentral = [middleOfStage + self.position, stageInfo.height]
        LightConeBeamLeftUpper = [
            LightConeBeamCentral[0] - c.LIGHT_SOURCE_RADIUS,
            LightConeBeamCentral[1],
        ]
        LightConeBeamRightUpper = [
            LightConeBeamCentral[0] + c.LIGHT_SOURCE_RADIUS,
            LightConeBeamCentral[1],
        ]
        spreadMult = math.sin(math.radians(self.spread / 2))
        # TODO: add the spread
        LightConeBeamLeftLower = [
            LightConeBeamCentral[0] - c.LIGHT_SOURCE_RADIUS,
            0,
        ]
        LightConeBeamRightLower = [
            LightConeBeamCentral[0] + c.LIGHT_SOURCE_RADIUS,
            0,
        ]

        points = [
            LightConeBeamLeftUpper,
            LightConeBeamRightUpper,
            LightConeBeamRightLower,
            LightConeBeamLeftLower,
        ]
        xPoints = [pos[0] for pos in points]
        yPoints = [pos[1] for pos in points]
        colours = [
            self.colour.getColourIndex(0),
            self.colour.getColourIndex(0),
            self.colour.getColourIndex(1),
            self.colour.getColourIndex(1),
        ]
        # TODO: make gradients nice
        ax.fill(xPoints, yPoints, colours[0], alpha=self.intensity / 11)
        pass


# Collection of lights and/or light groups
# Manages them a
class LightGroup:
    lights = []
    lightGroups = []

    # Constructor for a `LightGroup`
    def __init__(self, lights=[], lightGroups=[]):
        self.lights = lights
        self.lightGroups = lightGroups

    # Adds a light to the group
    def addLight(self, light):
        self.lights.append(light)

    # Adds a light group to the group
    def addLightGroup(self, lightGroup):
        self.lightGroups.append(lightGroup)

    # Iterates through all and draws them top down
    def drawTopDown(self, stageInfo: stage.StageDescriptor, ax: plt.Axes):
        for light in self.lights:
            light.drawTopDown(stageInfo, ax)
        for lightGroup in self.lightGroups:
            if lightGroup != self:
                lightGroup.drawTopDown(stageInfo, ax)

    # Iterates through all and draws them from the audience's perspective
    def draw2D(self, stageInfo: stage.StageDescriptor, ax: plt.Axes):
        for light in self.lights:
            light.draw2D(stageInfo, ax)
        for lightGroup in self.lightGroups:
            if lightGroup != self:
                lightGroup.draw2D(stageInfo, ax)
