import os
import sys
from typing import List

from detector import Detector
import state

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

sumoBinary = "/usr/local/share/sumo/bin/sumo-gui"
sumoCmd = [
    sumoBinary, "-c", "simple.sumocfg",
    "--step-length", "1",
    "--scale", ".2",
    "--error-log", "log.txt"]


class Simulator:
    def __init__(self) -> None:
        traci.start(sumoCmd, port=8813)
        traci.setOrder(1)
        self.detectors: List[Detector] = []
        self.file = open('data.txt', 'a+', newline='')

    def getDetectorList(self):
        l = []
        for d in self.detectors:
            l.append(d._id)
        return l

    def initDetectors(self):
        ids = traci.inductionloop.getIDList()
        for id in ids:
            d = Detector(id, state.Active())
            self.detectors.append(d)
        self.detectors[0].setState(state.Faulty())

    def get_all_readings(self):
        readings = {'time': traci.simulation.getTime()}
        for d in self.detectors:
            reading = d.get_reading()
            if(reading != None):
                readings[d._id] = reading
        return readings

    def get_detector_by_id(self, id):
        for d in self.detectors:
            if d._id == id:
                return d
        return None

    def set_detector_state(self, choice, state_name):
        d = self.get_detector_by_id(choice)
        if(d != None):
            module = __import__('state')
            class_: state.State = getattr(module, state_name)
            d.setState(class_)

    def simulate(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            self.file.write(str(self.get_all_readings()) + '\n')
            self.file.flush()

            traci.simulationStep()

        traci.close()
        print("done")
