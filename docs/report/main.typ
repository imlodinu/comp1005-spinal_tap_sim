#import "template.typ": project
#show: project.with(
  title: "Spinal Tap Concert Simulation",
  authors: (
    (
      name: "Lodinu Kalugalage",
      location: [Perth, Australia],
      email: "21442515@student.curtin.edu.au"
    ),
  ),
)

= Overview
_Spinal Tap Sim_ is is a program created to visualise and simulate the concert of the Mythical Band, _Spinal Tap_. This program is written in python3 (3.10.0) and uses a few dependencies such as matplotlib to simulate and visualise the band's concert based on a `.json` scene description. 

This program has a few features, based off the task specification:
  - Overhead view of the stage
  - Audience view of the stage
  - Rendering of the band's props
  - Lights with adjustable properties
  - Lightgroups for brush-like control over lights
  - Gradient lights 
  - Smoke machines with a few properties
  - Eulerian smoke simulation (through phiflow, which does use Moore neighbourhoods within the library)
  - Props loaded from arbitrary `.png` files
  - Props with scale and position
  - Backdrop selection between a file or solid colour
  - Choreography file specified in human readable `.json`
    - Adjustable stage size
    - All properties of objects can be adjusted from this file
  - Animation system with time intervals which repeats
= User Guide
== Running the program
To first run the program, run
```sh
python3 src/spinal-tap.py
```
in a bash compatible terminal. This will open the window up with the simulation and a progress bar in the terminal. The progress bar will show the progress of the simulation and is used because the simulation takes a while to run due to the smoke.

By default, the program will use the `assets/choreo/one.json` file as the scene description. This can be changed by passing the path to the scene file as an argument to the program. For example, to run the program with the scene `test.json` (test.json would be located at the root of the project structure as a sibling of README.md), run
```sh
python3 src/spinal-tap.py test.json
```

Additionally, to specify the number of iterations the program simulates other than the default 100, pass the number of iterations as the second argument. For example, to run the program with the scene `test.json` for 100 iterations, run
```sh
python3 src/spinal-tap.py test.json 100
```
But, if you wanted to use the default scene file, you can replace the scene parameter with `_`, like this.
```sh
python3 src/spinal-tap.py _ 100
```
#pagebreak()
= Traceability Matrix
#table(
  columns: (auto, auto, auto, auto),
  inset: 10pt,
  // align: horizon,
  [*Feature*], [*Code Reference*], [*Test Reference*], [*Completion*],
  "Light Objects", "src/light.py", "Tested with various different combinations of lights and their positions.", $checkmark$,
  "Light Groups", "src/light.py", "Tested by checking if lights changed properly when placed in a light group.", $checkmark$,
  "Gradient & Solid Colour Lights ", "src/light.py", "Tested by using a gradient light as well as solid light in scene descriptor.", $checkmark$,
)

= Discussion
= Showcase
= Conclusion
= Future Work
#lorem(20)
@netwok2020

#lorem(3)
#bibliography("refs.bib", style: "apa")