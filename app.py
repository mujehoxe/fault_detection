from threading import Thread
from libsumo.libsumo import simulation
from tui import Tui

from simulator import Simulator


def main():

    simulator = Simulator()
    simulator.initDetectors()

    Thread(target=simulator.simulate).start()

    choices = simulator.getDetectorList() + ["exit"]

    tui = Tui(choices, simulator)
    tui.run()


if __name__ == "__main__":
    main()
