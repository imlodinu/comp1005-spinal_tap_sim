# Dependencies on matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as pltpatches

import stage
import light as l
import colour as col
import constants as c


def main():
    fig, (topAx, audienceAx) = plt.subplots(
        2, 1, gridspec_kw={"height_ratios": [1, 10]}, figsize=(10, 10)
    )
    topAx.set_aspect("equal")
    audienceAx.set_aspect("equal")

    # Create a stage
    stageInfo = stage.StageDescriptor(500, 500, None)
    topAx.fill(
        [0, stageInfo.width, stageInfo.width, 0],
        [0, 0, c.LIGHT_SOURCE_DIAMETER, c.LIGHT_SOURCE_DIAMETER],
        color="black",
    )
    audienceAx.fill(
        [0, 0, stageInfo.width, stageInfo.width],
        [0, stageInfo.height, stageInfo.height, 0],
        color="black",
    )

    # Create lights
    light1 = l.Light(col.Colour("red"), 0.0, 90, 11, 25)
    light2 = l.Light(col.Colour("blue"), 100.0, 90, 5, 25)

    lg = l.LightGroup([light1, light2])

    lg.drawTopDown(stageInfo, topAx)
    lg.draw2D(stageInfo, audienceAx)

    plt.suptitle("STAGE VIEW", fontsize="18")
    plt.show()


if __name__ == "__main__":
    main()
