# Spinal Tap Concert Simulation

## Synopsis

Spinal Tap concert simulation for COMP1005/5005 assignment

## Contents

README - readme file for Spinal Tap Concert Simulation
assets/  - folder with assets related to the project
    backdrops/ - folder with backdrops
    choreo/    - folder with a choreography file (.json)
    props/     - image assets for the props
docs/    - folder with documents
    report/    - a folder with a report built on typst (like LaTeX but more functional)
    2023 S2 FOP Assignment - v1.0.pdf - assignment specification
src/     - folder with code
    colour.py - a file with colour related things for consumption in the project
    constants.py - a file with some constants used in the program
    director.py - a big overarching class that manages choreography, drawing and cleanup of the modules
    light.py - a file that contains light definitions as well as light groups
    prop.py - a file that contains the `Prop` class, which is basically a sprite
    smoke.py - a file that contains the smoke related things, and makes use of phiflow (physics is not a strong suit of mine)
    spinal-tap.py - the entry point for the program
    stage.py - a file that contains the `Stage` class, which manages the backdrop, stage definition, and sizing
    util.py - a file that contains some utility functions
.editorconfig - a file that contains some editor settings
.gitignore - a file that contains files to ignore in git
README.md - this file

## Dependencies

python3 and modules (3.10.0, the language project is written in)
matplotlib (used for plotting)
numpy (used for ndarray and other useful things)
scikit-image (used for image processing)
PIL (pillow, included with matplotlib and used for image loading)
phiflow (used for the smoke simulation's equations, justified use as the task is not requesting to implement the math from scratch)
tqdm (used for terminal status indicator)

## Version information

17/04/2023 - initial version of Spinal Tap Concert program
20/05/2023 - completed task requirements for Spinal Tap Concert program
