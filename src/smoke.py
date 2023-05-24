# smoke.py
# Lodinu Kalugalage
#
# Description: This file contains the smoke related classes

# dependencies
import numpy as np
from matplotlib import pyplot as plt
import phi.flow as pf

from typing import Tuple  # Included with python

import colour as col
import constants as c
import stage as stg


# A definition for a smoke machine
class SmokeMachine:
    position = None  # [x, y] position of the smoke machine
    # direction = None  # [x, y] direction the smoke machine is facing
    intensity = None  # 0-11, intensity of the smoke machine

    def __init__(self, position, intensity):
        self.position = position
        # self.direction = direction
        self.intensity = intensity


# Volume class with phi
class Volume:
    stageInfo: stg.StageDescriptor  # Stage descriptor

    x: int
    y: int

    timeStep = 1.0
    decay = 0.0

    bound: pf.Box  # Boundary of the volume
    smoke: pf.CenteredGrid  # Smoke density
    # Staggered grid is a grid where the values are stored at the edges of the grid
    # Which means it does moore neighbour interpolation
    velocity: pf.StaggeredGrid  # Velocity field

    # Constructor for a `Volume`
    def __init__(self, stageInfo: stg.StageDescriptor):
        self.stageInfo = stageInfo
        self.bound = pf.Box(x=stageInfo.width, y=stageInfo.height)
        self.x, self.y = int(stageInfo.width * c.SMOKE_SIM_RESOLUTION), int(
            stageInfo.height * c.SMOKE_SIM_RESOLUTION
        )

        self.smoke = pf.CenteredGrid(
            0,
            pf.extrapolation.BOUNDARY,
            x=self.x,
            y=self.y,
            bounds=self.bound,
        )
        self.velocity = pf.StaggeredGrid(
            0,
            pf.extrapolation.ZERO,
            x=self.x,
            y=self.y,
            bounds=self.bound,
        )

    def step(self, inflow: pf.field.SampledField):
        # Complicated phsics stuff simplified with phiflow
        # (its faster too)
        smoke = (
            pf.advect.mac_cormack(self.smoke, self.velocity, dt=self.timeStep) + inflow
        )
        smoke = smoke * (1 - self.decay)
        buoyancy_force = (smoke * (0, 4)) @ (self.velocity)
        velocity = (
            pf.advect.semi_lagrangian(self.velocity, self.velocity, dt=self.timeStep)
            + buoyancy_force
        )
        velocity, _ = pf.fluid.make_incompressible(velocity)
        self.smoke, self.velocity = smoke, velocity  # type: ignore


# SmokeMachine Volume
class SmokeMachineVolume:
    stageInfo: stg.StageDescriptor
    volume: Volume  # Volume object
    machines = []  # List of SmokeMachine objects
    smokeColour: Tuple[float, float, float] = (1, 1, 1)

    # Constructor for a `SmokeMachineVolume`
    def __init__(self, stageInfo, col: Tuple[float, float, float] = (1, 1, 1)):
        self.stageInfo = stageInfo
        self.volume = Volume(stageInfo)
        self.smokeColour = col

    # Adds a `SmokeMachine` to the volume
    def addMachine(self, machine: SmokeMachine):
        self.machines.append(machine)

    # Step simulation
    def step(self):
        # Objects
        inflow = None
        for machine in self.machines:
            # Add to list
            addTo = (machine.intensity / 11) * pf.CenteredGrid(
                pf.Sphere(x=machine.position[0], y=machine.position[1], radius=c.SMOKE_MACHINE_RADIUS),  # type: ignore
                pf.extrapolation.BOUNDARY,
                x=self.volume.x,
                y=self.volume.y,
                bounds=self.volume.bound,
            )
            if inflow == None:
                inflow = addTo
            else:
                inflow += addTo
        # Create inflow
        self.volume.step(inflow)  # type: ignore
        pass

    # Draws the volume
    def draw(self, ax: plt.Axes):
        vals = np.sum(self.volume.smoke.values.numpy("y,x,inflow_loc")[...], axis=2)
        cmap = col.getOrMakeCMAP(
            (*self.smokeColour, 0), (*self.smokeColour, 1), "smokeTransparency"
        )
        ax.imshow(
            vals,
            cmap=cmap,
            interpolation="bicubic",
            origin="lower",
            extent=[0, self.stageInfo.width, 0, self.stageInfo.height],
        )
