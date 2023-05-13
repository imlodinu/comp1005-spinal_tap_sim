# Dependencies on matplotlib
import matplotlib.pyplot as plt
import numpy as np

import stage as stg
import light as l
import colour as col
import constants as c


def main():
    # Create a stage
    stageInfo = stg.StageDescriptor(500, 500, None)

    stage = stg.StageDraw(stageInfo)

    # Create lights
    light1 = l.Light(col.Colour("blue"), 100.0, 90, 10, 40)
    light2 = l.Light(col.Colour(["purple", "blue"]), 0.0, 90, 9, 25)

    lg = l.LightGroup([light1, light2])

    lg.drawTopDown(stageInfo, stage.topAx)
    lg.draw2D(stageInfo, stage.sideAx)

    plt.suptitle("STAGE VIEW", fontsize="18")
    plt.show()


if __name__ == "__main__":
    main()
