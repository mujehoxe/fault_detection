import os
import sys
from state import State

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


class Detector:
    def __init__(self, id, state: State):
        self._id = id
        self.subscribed = False
        self._state = state
        state.setContext(self)
        self.hour_of_data = []

    def setState(self, state: State, lock):
        if(self._state.name != state.name):
            with lock:
                self._state = state
                state.setContext(self)

    def subscribe(self):
        if(self.subscribed == False):
            self.subscribed = True
            traci.inductionloop.subscribe(
                self._id,
                [traci.constants.LAST_STEP_VEHICLE_DATA])

    def unsubscribe(self):
        if(self.subscribed == True):
            self.subscribed = False
            traci.inductionloop.unsubscribe(self._id)

    def get_reading(self, lock):
        with lock:
            r = self._state.get_reading()
            if(r):
                self.hour_of_data.append(len(r))
                return r

    def init_hour_of_data(self):
        self.hour_of_data = []

    def get_sum_hour_of_data(self):
        return sum(self.hour_of_data)

    def calculate_vehicle_speed(self, veh_data):
        veh_length = veh_data[1]
        entry_time = veh_data[2]
        exit_time = veh_data[3]
        return veh_length/(exit_time - entry_time)

    def mps_to_kmh(self, speed):
        return speed * 3.6
