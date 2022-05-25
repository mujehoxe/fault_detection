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
        self.setState(state)

    def setState(self, state: State):
        self._state = state
        self._state.setContext(self)

    def subscribe(self):
        traci.inductionloop.subscribe(
            self._id,
            [traci.constants.LAST_STEP_VEHICLE_DATA])

    def unsubscribe(self):
        traci.inductionloop.unsubscribe(self._id)

    def get_reading(self):
        return self._state.get_reading()

    def get_speed_reading(self):
        reading = self.get_reading()
        speeds = []
        if(isinstance(reading, list)):
            for veh_data in reading:
                if veh_data[3] != -1:
                    speed = self.calculate_vehicle_speed(veh_data)
                    speeds.append(self.mps_to_kmh(speed))
        return speeds

    def calculate_vehicle_speed(self, veh_data):
        veh_length = veh_data[1]
        entry_time = veh_data[2]
        exit_time = veh_data[3]
        return veh_length/(exit_time - entry_time)

    def mps_to_kmh(self, speed):
        return speed * 3.6
