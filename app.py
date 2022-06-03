from threading import Thread
from daily_aggregator import DailyAggregator
from sender import Sender
from tui import Tui

from simulator import Simulator


def main():

    simulator = Simulator()
    simulator.initDetectors()

    DailyAggregator(simulator)
    Thread(target=simulator.simulate).start()
    Sender(simulator)

    choices = simulator.getDetectorList() + ["exit"]

    tui = Tui(choices, simulator)
    tui.run()


if __name__ == "__main__":
    main()
