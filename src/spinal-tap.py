# Dependencies on matplotlib
import matplotlib.pyplot as plt

from tqdm import tqdm  # Used to make a nice scrolling thing in the terminal

import sys  # Included with python
import os  # Included with python

import constants
import director
import util


def main():
    # Loading the information from assets/
    choreoFile = (
        "../assets/choreo/one.json"
        if not len(sys.argv) > 1 or sys.argv[1] == "_"
        else sys.argv[1]
    )
    choreo = director.Choreography.loadFromFile(util.getPath(choreoFile))
    choreo.parse()
    plt.suptitle("STAGE VIEW", fontsize="18")

    if constants.CACHE_IMAGES:
        os.makedirs("_simcache", exist_ok=True)

    # Accepting a command line argument for the number of simulations to run or default to 100
    simCount = 100 if not len(sys.argv) > 2 else int(sys.argv[2])
    for i in tqdm(range(simCount)):
        choreo.step()
        choreo.draw()
        plt.draw()
        plt.pause(0.1)
        if constants.CACHE_IMAGES:
            name = f"_simcache/{i}.png"
            choreo.stage.snapshot(name)
        choreo.clean()


if __name__ == "__main__":
    main()
