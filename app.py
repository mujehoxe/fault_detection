import os
import sys
from threading import Thread
from tui import Tui

from simulator import Simulator
from state import *


def loop(simulator):
    while(True):
        line = input(">>> ").split()
        expr = "simulator.set_detector_state('" + \
            line[0] + "', '" + \
            line[1] + "')"
        print(line)
        eval(expr)


def main():

    simulator = Simulator()
    simulator.initDetectors()

    Thread(target=simulator.simulate).start()

    Thread(target=loop, args=(simulator,)).start()

    choices = simulator.getDetectorList() + ["exit"]

    #tui = Tui(choices, simulator)
    # tui.run()


if __name__ == "__main__":
    main()
