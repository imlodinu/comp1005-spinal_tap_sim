# Dependencies on matplotlib
import matplotlib.pyplot as plt

from tqdm import tqdm  # Used to make a nice scrolling thing in the terminal

import sys  # Included with python
import os  # Included with python

import director
import util


def main():
    # Loading the information from assets/
    choreo = director.Choreography.loadFromFile(
        util.getPath("../assets/choreo/one.json")
    )
    choreo.parse()
    plt.suptitle("STAGE VIEW", fontsize="18")

    # Accepting a command line argument for the number of simulations to run or default to 100
    simCount = 100 if not len(sys.argv) > 1 else int(sys.argv[1])
    for i in tqdm(range(simCount)):
        choreo.step()
        choreo.draw()
        plt.draw()
        plt.pause(0.1)
        choreo.clean()


if __name__ == "__main__":
    main()
