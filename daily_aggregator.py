import math
import pandas as pd

from simulator import Simulator


class DailyAggregator:

    def __init__(self, simulator: Simulator) -> None:
        self.simulator = simulator
        simulator.add_observer(self)

        self.traffic_scale = self.csv_to_df('traffic-scale-day-hour.csv')
        self.hours_in_day = len(self.traffic_scale.columns)
        self.days_in_week = len(self.traffic_scale.index)

        self.current_hour = 0
        self.current_day = 0

        self.hourly_reading = {'day': [], 'interval': []}
        self.daily_reading = {}

    def update(self, data):
        self.current_reading = data

        self.hour_reached()
        self.day_reached()
        self.week_reached()

    def week_reached(self):
        if self.is_week_reached():
            self.simulator.remove_observer(self)
            pd.DataFrame(self.hourly_reading).to_csv('hourly.csv')
            pd.DataFrame(
                self.daily_reading.values(),
                columns=self.traffic_scale.columns,
                index=self.traffic_scale.index).to_csv('daily.csv')

    def is_week_reached(self):
        return self.current_day == self.days_in_week

    def day_reached(self):
        if self.is_day_reached():
            print(self.hourly_reading)
            print(self.daily_reading)
            self.current_day += 1
            self.current_hour = 0
            if(not self.is_week_reached()):
                self.simulator.set_traffic_scale(
                    self.get_current_interval_scale())

    def hour_reached(self):
        if self.is_hour_reached() and not self.is_week_reached():
            if self.current_reading['time'] != 0:
                self.current_hour += 1
            if self.current_hour != 0:
                self.update_hourly_reading()
                detector = self.simulator.get_detector_by_id('sen1')
                if detector != None:
                    self.update_daily_reading(detector.get_sum_hour_of_data())
                    detector.init_hour_of_data()
            if not self.is_day_reached():
                self.simulator.set_traffic_scale(
                    self.get_current_interval_scale())

    def is_day_reached(self):
        return self.current_hour != 0 and (self.current_hour % self.hours_in_day == 0)

    def is_hour_reached(self):
        return math.floor(self.current_reading['time'] % 3600) == 0

    def update_hourly_reading(self):
        self.hourly_reading['day'].append(self.get_current_day_name())
        self.hourly_reading['interval'].append(self.get_previous_interval())
        for d in self.simulator.detectors:
            self.create_dict_field_if_not_exist(d._id, self.hourly_reading, [])
            self.hourly_reading[d._id].append(d.get_sum_hour_of_data())

    def update_daily_reading(self, reading):
        self.create_dict_field_if_not_exist(
            self.current_day, self.daily_reading, [])
        self.daily_reading[self.current_day].append(reading)

    def create_dict_field_if_not_exist(self, field, dic, value):
        if not field in dic:
            dic[field] = value

    def get_current_interval(self):
        return str(self.current_hour) + '-' + str((self.current_hour + 1) % self.hours_in_day)

    def get_previous_interval(self):
        return str(self.current_hour - 1) + '-' + str(self.current_hour % self.hours_in_day)

    def get_current_interval_scale(self):
        return self.traffic_scale[self.get_current_interval()][self.current_day] / 100

    def get_current_day_name(self):
        return self.traffic_scale.index[self.current_day]

    def csv_to_df(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path, index_col='day')
