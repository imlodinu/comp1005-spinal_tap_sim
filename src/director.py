# director.py
# Lodinu Kalugalage
#
# Description: This file contains the director class which is used to direct the scene.

# Dependencies
import json  # Included with python

import light
import prop
import smoke
import stage as stg
import colour
import util


class Choreography:
    jsonBlock: str
    objectBins = {
        "lights": {},
        "props": {},
        "smokeMachines": {},
        "lightGroups": {},
        "smokeMachineVolumes": {},
    }
    stageInfo: stg.StageDescriptor
    stage: stg.StageDraw

    objectMapping = {
        "light": [light.Light, "lights"],
        "prop": [prop.Prop, "props"],
        "smokemachine": [smoke.SmokeMachine, "smokeMachines"],
        "lightgroup": [light.LightGroup, "lightGroups"],
        "smokemachinevolume": [smoke.SmokeMachineVolume, "smokeMachineVolumes"],
    }

    steps = {}

    # Constructor for a `Choreography`
    def __init__(self, jsonBlock: str):
        self.jsonBlock = jsonBlock

    # Loads a choreography from a file
    @staticmethod
    def loadFromFile(filename: str):
        with open(util.getPath(filename), "r") as f:
            return Choreography(f.read())

    # Parses the json
    def parse(self):
        loadedJson = json.loads(self.jsonBlock)
        self.stageInfo = stg.StageDescriptor(
            loadedJson["width"], loadedJson["height"], loadedJson["backdrop"]
        )
        intObjectBins = {
            "lights": {},
            "props": {},
            "smokeMachines": {},
            "lightGroups": {},
            "smokeMachineVolumes": {},
        }
        for key in loadedJson["objects"]:
            obj = loadedJson["objects"][key]
            if obj["type"] in self.objectMapping:
                intObjectBins[self.objectMapping[obj["type"]][1]][key] = obj
            else:
                print("Unknown object type: " + obj["type"])

        for light_key in intObjectBins["lights"]:
            lightDef = intObjectBins["lights"][light_key]
            lightObj = light.Light(
                colour.Colour(lightDef["colour"]),
                lightDef["position"],
                lightDef["direction"],
                lightDef["intensity"],
            )
            self.objectBins["lights"][light_key] = lightObj

        for prop_key in intObjectBins["props"]:
            propDef = intObjectBins["props"][prop_key]
            propObj = prop.propFromFile(propDef["img"])
            propObj.scale = propDef["scale"]
            propObj.position = propDef["position"]
            self.objectBins["props"][prop_key] = propObj

        for smokeMachine_key in intObjectBins["smokeMachines"]:
            smokeMachineDef = intObjectBins["smokeMachines"][smokeMachine_key]
            smokeMachineObj = smoke.SmokeMachine(
                smokeMachineDef["position"], smokeMachineDef["intensity"]
            )
            self.objectBins["smokeMachines"][smokeMachine_key] = smokeMachineObj

        for lightGroup_key in intObjectBins["lightGroups"]:
            lightGroupDef = intObjectBins["lightGroups"][lightGroup_key]
            lightGroupObj = light.LightGroup([], [])
            for light_key in lightGroupDef["lights"]:
                lightGroupObj.lights.append(self.objectBins["lights"][light_key])
            self.objectBins["lightGroups"][lightGroup_key] = lightGroupObj

        for smokeMachineVolume_key in intObjectBins["smokeMachineVolumes"]:
            smokeMachineVolumeDef = intObjectBins["smokeMachineVolumes"][
                smokeMachineVolume_key
            ]
            smokeMachineVolumeObj = smoke.SmokeMachineVolume(
                self.stageInfo,
                smokeMachineVolumeDef["colour"],
            )
            for smokeMachine_key in smokeMachineVolumeDef["smokemachines"]:
                smokeMachineVolumeObj.addMachine(
                    self.objectBins["smokeMachines"][smokeMachine_key]
                )
            self.objectBins["smokeMachineVolumes"][
                smokeMachineVolume_key
            ] = smokeMachineVolumeObj
        self.stage = stg.StageDraw(self.stageInfo)

        self.steps = loadedJson["steps"]

    def draw(self):
        # Order:
        # Draw background
        # Draw props
        # Draw smoke
        # Draw lights
        self.stage.draw()

        for prop_key in self.objectBins["props"]:
            propObj = self.objectBins["props"][prop_key]
            propObj.draw(self.stage.sideAx)

        for smokeMachineVolume_key in self.objectBins["smokeMachineVolumes"]:
            smokeMachineVolumeObj = self.objectBins["smokeMachineVolumes"][
                smokeMachineVolume_key
            ]
            smokeMachineVolumeObj.draw(self.stage.sideAx)

        for lightg_key in self.objectBins["lightGroups"]:
            lightGroupObj = self.objectBins["lightGroups"][lightg_key]
            lightGroupObj.drawTopDown(self.stageInfo, self.stage.topAx)
            lightGroupObj.draw2D(self.stageInfo, self.stage.sideAx)

    stepFrame = 0
    buffering = (
        1  # we start off with one to have at least one frame with original state
    )

    # Steps through things inside
    def step(self):
        for smokeMachineVolume_key in self.objectBins["smokeMachineVolumes"]:
            smokeMachineVolumeObj = self.objectBins["smokeMachineVolumes"][
                smokeMachineVolume_key
            ]
            smokeMachineVolumeObj.step()

        # We use buffering so that we can alter the speed of the choreography
        if self.buffering > 0:
            self.buffering -= 1
        # If we still need to buffer, stop updating
        if self.buffering > 0:
            return

        thisStep = self.steps[self.stepFrame]
        for step in thisStep:
            t = step[0]
            # ideally there'd be a switch statement but python doesn't have one
            # (it has match but it doesn't work nicely)
            if t == "light":
                name = step[1]
                lightObj = self.objectBins["lights"][name]
                action = step[2]
                arg = step[3]
                if action == "position":
                    if arg == "add":
                        lightObj.position += step[4]
                    elif arg == "set":
                        lightObj.position = step[4]
                    elif arg == "sub":
                        lightObj.position -= step[4]
                    else:
                        print("Unknown light action: " + arg)
                elif action == "direction":
                    if arg == "add":
                        lightObj.direction += step[4]
                    elif arg == "set":
                        lightObj.direction = step[4]
                    elif arg == "sub":
                        lightObj.direction -= step[4]
                    else:
                        print("Unknown light action: " + arg)
                elif action == "intensity":
                    if arg == "add":
                        lightObj.intensity += step[4]
                    elif arg == "set":
                        lightObj.intensity = step[4]
                    elif arg == "sub":
                        lightObj.intensity -= step[4]
                    else:
                        print("Unknown light action: " + arg)
                elif action == "colour":
                    lightObj.colour = colour.Colour(step[3])
                pass
            elif t == "prop":
                name = step[1]
                propObj = self.objectBins["props"][name]
                action = step[2]
                arg = step[3]
                if action == "position":
                    if arg == "add":
                        propObj.position = (
                            propObj.position[0] + step[4][0],
                            propObj.position[1] + step[4][1],
                        )
                    elif arg == "set":
                        propObj.position = (
                            step[4][0],
                            step[4][1],
                        )
                    elif arg == "sub":
                        propObj.position = (
                            propObj.position[0] - step[4][0],
                            propObj.position[1] - step[4][1],
                        )
                    else:
                        print("Unknown prop action: " + arg)
                elif action == "scale":
                    if arg == "add":
                        propObj.scale += step[4]
                    elif arg == "set":
                        propObj.scale = step[4]
                    elif arg == "sub":
                        propObj.scale -= step[4]
                    else:
                        print("Unknown prop action: " + arg)
                pass
            elif t == "smokemachine":
                name = step[1]
                smokemachineObj = self.objectBins["smokeMachines"][name]
                action = step[2]
                arg = step[3]
                if action == "position":
                    if arg == "add":
                        smokemachineObj.position = (
                            smokemachineObj.position[0] + step[4][0],
                            smokemachineObj.position[1] + step[4][1],
                        )
                    elif arg == "set":
                        smokemachineObj.position = (
                            step[4][0],
                            step[4][1],
                        )
                    elif arg == "sub":
                        smokemachineObj.position = (
                            smokemachineObj.position[0] - step[4][0],
                            smokemachineObj.position[1] - step[4][1],
                        )
                    else:
                        print("Unknown smokemachine action: " + arg)
                elif action == "intensity":
                    if arg == "add":
                        smokemachineObj.intensity += step[4]
                    elif arg == "set":
                        smokemachineObj.intensity = step[4]
                    elif arg == "sub":
                        smokemachineObj.intensity -= step[4]
                    else:
                        print("Unknown smokemachine action: " + arg)
                pass
            elif t == "lightgroup":
                pass
            elif t == "smokemachinevolume":
                pass
            elif t == "buffer":
                self.buffering = step[1]
            else:
                print("Unknown step type: " + t)

        # Animations are looping, and will be reset to the first frame after it's done
        # with the sequence
        self.stepFrame = (self.stepFrame + 1) % len(self.steps)

    # Cleans the stage for next frame
    def clean(self):
        self.stage.clean()
