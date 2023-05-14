# smoke.py
# Lodinu Kalugalage
#
# Description: This file contains the smoke related classes

# dependencies
import numpy as np
from functools import reduce

# import stage as stg
import colour as col
import util as u
import constants as c
import stage as stg

import math


# A definition for a smoke machine
class SmokeMachine:
    position = None  # [x, y] position of the smoke machine
    direction = None  # 0-360 degrees, direction the smoke machine is facing
    intensity = None  # 0-11, intensity of the smoke machine

    def __init__(self, position, direction, intensity):
        self.position = position
        self.direction = direction
        self.intensity = intensity


transparencyCMAP = col.getOrMakeCMAP((1, 1, 1, 0), (1, 1, 1, 1), "smokeTransparency")


# Converts from a 2D coordinate to a 1D coordinate in the arrays
def _coordToIndex(stageInfo: stg.StageDescriptor, x, y):
    return y * stageInfo.width + x


# Converts from a 1D coordinate to a 2D coordinate in the arrays
def _indexToCoord(stageInfo: stg.StageDescriptor, i):
    return (i % stageInfo.width, i // stageInfo.width)


# Boundary operations
def _setBoundary(
    boundaryCondition: int,
    values: np.ndarray[np.float64],
    stageInfo: stg.StageDescriptor,
):
    for index in range(1, stageInfo.width - 1):
        # Balances x
        values[_coordToIndex(0, index)] = (
            -1 if boundaryCondition == 1 else 1
        ) * values[_coordToIndex(1, index)]
        values[_coordToIndex(stageInfo.width - 1, index)] = (
            -1 if boundaryCondition == 1 else 1
        ) * values[_coordToIndex(stageInfo.width - 2, index)]
        # Balances y
        values[_coordToIndex(index, 0)] = (
            -1 if boundaryCondition == 2 else 1
        ) * values[_coordToIndex(index, 1)]
        values[_coordToIndex(index, stageInfo.height - 1)] = (
            -1 if boundaryCondition == 2 else 1
        ) * values[_coordToIndex(index, stageInfo.height - 2)]

    # Balances corners
    values[_coordToIndex(0, 0)] = 0.5 * (
        values[_coordToIndex(1, 0)] + values[_coordToIndex(0, 1)]
    )
    values[_coordToIndex(0, stageInfo.height - 1)] = 0.5 * (
        values[_coordToIndex(1, stageInfo.height - 1)]
        + values[_coordToIndex(0, stageInfo.height - 2)]
    )
    values[_coordToIndex(stageInfo.width - 1, 0)] = 0.5 * (
        values[_coordToIndex(stageInfo.width - 2, 0)]
        + values[_coordToIndex(stageInfo.width - 1, 1)]
    )
    values[_coordToIndex(stageInfo.width - 1, stageInfo.height - 1)] = 0.5 * (
        values[_coordToIndex(stageInfo.width - 2, stageInfo.height - 1)]
        + values[_coordToIndex(stageInfo.width - 1, stageInfo.height - 2)]
    )


# Function for volume advection and diffusion
def _linearSolver(
    boundaryCondition: int,
    values: np.ndarray[np.float64],
    previousValues: np.ndarray[np.float64],
    a: float,
    c: float,
    stageInfo: stg.StageDescriptor,
    iterationAmount: int,
):
    reciprocalC = 1 / c
    # Gauss-Seidel relaxation is iterative
    for index in range(iterationAmount):
        # For each cell (we ignore the edges)
        for y in range(1, stageInfo.height - 1):
            for x in range(1, stageInfo.width - 1):
                index = _coordToIndex(stageInfo, x, y)

                # Van-Neumann neighbourhoods
                # Get the values of the cell and its neighbours
                left = values[index - 1]
                right = values[index + 1]
                top = values[index - stageInfo.width]
                bottom = values[index + stageInfo.width]

                # Calculate the new value of the cell
                values[index] = (
                    previousValues[index]
                    + a * (left + right + top + bottom) * reciprocalC
                )
        _setBoundary(boundaryCondition, values, stageInfo)


# Function for volume diffusion
def _diffuse(
    boundaryCondition: int,
    stageInfo: stg.StageDescriptor,
    iterationAmount: int,
    values: np.ndarray[np.float64],
    beforeValues: np.ndarray[np.float64],
    diffusion: float,
    deltaTime: float,
):
    # Scale the amount we diffuse by the delta time and size
    diffuseAmount = diffusion * deltaTime * stageInfo.width * stageInfo.height
    _linearSolver(
        boundaryCondition,
        values,
        beforeValues,
        diffuseAmount,
        deltaTime,
        stageInfo,
        iterationAmount,
    )


# Function for volume projection (mass conservation)
def _project(
    stageInfo: stg.StageDescriptor,
    iterationAmount: int,
    xValues: np.ndarray[np.float64],
    yValues: np.ndarray[np.float64],
    pressureValues: np.ndarray[np.float64],
    divergentValues: np.ndarray[np.float64],
):
    for y in range(1, stageInfo.height - 1):
        for x in range(1, stageInfo.width - 1):
            index = _coordToIndex(stageInfo, x, y)
            # Calculate the divergence of the cell
            divergentValues[index] = (
                -0.5
                * (
                    xValues[index + 1]
                    - xValues[index - 1]
                    + yValues[index + stageInfo.width]
                    - yValues[index - stageInfo.width]
                )
                / stageInfo.width
            )
            # Set the pressure of the cell to 0
            pressureValues[index] = 0

    # Set the boundaries of the divergence and pressure
    _setBoundary(0, divergentValues, stageInfo)
    _setBoundary(0, pressureValues, stageInfo)
    _linearSolver(0, pressureValues, divergentValues, 1, 6, stageInfo, iterationAmount)

    # For each cell
    for y in range(1, stageInfo.height - 1):
        for x in range(1, stageInfo.width - 1):
            index = _coordToIndex(stageInfo, x, y)
            # Calculate the pressure gradient
            xValues[index] -= (
                0.5
                * stageInfo.width
                * (pressureValues[index + 1] - pressureValues[index - 1])
            )
            yValues[index] -= (
                0.5
                * stageInfo.width
                * (
                    pressureValues[index + stageInfo.width]
                    - pressureValues[index - stageInfo.width]
                )
            )

    # Set the boundaries of the x and y velocities
    _setBoundary(1, xValues, stageInfo)
    _setBoundary(2, yValues, stageInfo)


# Function for volume advection
# Advection is like diffusion but actually moves the smoke
#   semi-Lagrangian method
def _advect(
    boundaryCondition: int,
    densities: np.ndarray[np.float64],
    previousDensities: np.ndarray[np.float64],
    xVelocities: np.ndarray[np.float64],
    yVelocities: np.ndarray[np.float64],
    stageInfo: stg.StageDescriptor,
    deltaTime: float,
):
    deltaX = deltaTime * stageInfo.width
    deltaY = deltaTime * stageInfo.height

    for x in range(1, stageInfo.width - 1):
        for y in range(1, stageInfo.height - 1):
            index = _coordToIndex(stageInfo, x, y)

            # Calculate the position of the cell
            xPosition = x - deltaX * xVelocities[index]
            yPosition = y - deltaY * yVelocities[index]

            # Clamp the position to the stage
            if xPosition < 0.5:
                xPosition = 0.5
            elif xPosition > stageInfo.width - 1.5:
                xPosition = stageInfo.width - 1.5
            if yPosition < 0.5:
                yPosition = 0.5
            elif yPosition > stageInfo.height - 1.5:
                yPosition = stageInfo.height - 1.5

            # Get the position of the cell
            x0 = math.floor(xPosition)
            x1 = x0 + 1
            y0 = math.floor(yPosition)
            y1 = y0 + 1

            # Get the interpolation factors
            s1 = xPosition - x0
            s0 = 1 - s1
            t1 = yPosition - y0
            t0 = 1 - t1

            # Interpolate the density
            densities[index] = s0 * (
                t0 * previousDensities[_coordToIndex(stageInfo, x0, y0)]
                + t1 * previousDensities[_coordToIndex(stageInfo, x0, y1)]
            ) + s1 * (
                t0 * previousDensities[_coordToIndex(stageInfo, x1, y0)]
                + t1 * previousDensities[_coordToIndex(stageInfo, x1, y1)]
            )
    _setBoundary(boundaryCondition, densities, stageInfo)


# Simulates fluid
class Volume:
    stageInfo = None  # StageDescriptor object

    nCells = 0  # Number of cells in the volume

    deltaTime = 0.1  # Time between simulations
    viscosity = 0.0  # Viscosity of the smoke
    diffusion = 0.0  # Diffusion of the smoke

    xN = None  # List of x velocities of the cells
    yN = None  # List of y velocities of the cells
    dN = None  # List of smoke concentrations of the cells

    xB = None  # List of previous x velocities of the cells
    yB = None  # List of previous y velocities of the cells
    dB = None  # List of previous smoke concentrations of the cells

    # Constructor for a `Volume`
    def __init__(self, stageInfo, deltaTime, viscosity, diffusion):
        self.stageInfo = stageInfo
        self.nCells = stageInfo.width * stageInfo.height

        self.deltaTime = deltaTime
        self.viscosity = viscosity
        self.diffusion = diffusion

        self.yN = np.zeros(self.nCells)
        self.xN = np.zeros(self.nCells)
        self.dN = np.zeros(self.nCells)

        self.yB = np.zeros(self.nCells)
        self.xB = np.zeros(self.nCells)
        self.dB = np.zeros(self.nCells)

    # Adds smoke to the volume
    def addSmokeConcentration(self, pX: int, pY: int, concentration: float):
        index = _coordToIndex(pX, pY)
        self.dN[index] += concentration

    # Adds velocity to the volume
    def addVelocity(self, pX: int, pY: int, vX: float, vY: float):
        index = _coordToIndex(pX, pY)
        self.xN[index] += vX
        self.yN[index] += vY

    # Step simulation
    def step():
        pass
