# Dependencies on matplotlib
import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm

import director


def main():
    choreo = director.Choreography.loadFromFile("assets/choreo/one.json")
    choreo.parse()
    plt.suptitle("STAGE VIEW", fontsize="18")

    for i in tqdm(range(100)):
        choreo.step()
        choreo.draw()
        plt.draw()
        plt.pause(0.1)
        choreo.clean()


if __name__ == "__main__":
    main()
