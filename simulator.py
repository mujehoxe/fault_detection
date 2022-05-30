import os
import sys

import threading
from typing import List

from detector import Detector
import state

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
from traci.connection import Connection

sumoBinary = "/usr/local/share/sumo/bin/sumo"
sumoCmd = [
    sumoBinary, "-c", "simple.sumocfg",
    "--step-length", "1",
    "--scale", ".2",
    "--no-warnings", "true",
    "--no-step-log",
    "--error-log", "log.txt"]


class Observable:

    observers = []

    def add_observer(self, o):
        self.observers.append(o)

    def notify_observers(self, msg):
        for o in self.observers:
            o.send(msg)


class Simulator(Observable):
    def __init__(self) -> None:
        traci.start(sumoCmd, port=8813, label="sim1")
        traci.setOrder(1)
        self.detectors: List[Detector] = []
        self.file = open('data.txt', 'a+', newline='')
        self.lock = threading.Lock()

    def initDetectors(self):
        ids = traci.inductionloop.getIDList()
        for id in ids:
            d = Detector(id, state.Active())
            self.detectors.append(d)
        self.detectors[0].setState(state.Faulty(), self.lock)

    def getDetectorList(self):
        l = []
        for d in self.detectors:
            l.append(d._id)
        return l

    def get_all_readings(self):
        readings = {'time': self.get_time()}
        for d in self.detectors:
            reading = d.get_reading(self.lock)
            if(reading != None):
                readings[d._id] = reading
        return readings

    def get_time(self):
        with self.lock:
            return traci.simulation.getTime()

    def get_detector_by_id(self, id):
        for d in self.detectors:
            if d._id == id:
                return d

    def set_detector_state(self, detector_id, state_name):
        detector = self.get_detector_by_id(detector_id)
        module = __import__('state')
        class_: state.State = getattr(module, state_name)()
        detector.setState(class_, self.lock)

    def simulate(self):
        def get_min_num():
            with self.lock:
                return traci.simulation.getMinExpectedNumber()

        while get_min_num() > 0:
            data = self.get_all_readings()
            self.file.write(str(data) + '\n')
            self.file.flush()

            self.notify_observers(data)

            with self.lock:
                traci.simulationStep()

        with self.lock:
            traci.close()
        print("done")
