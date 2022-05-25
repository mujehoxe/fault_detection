
from time import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd


file = open('./data.txt', 'r')

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
ax.set_xlim([0, 4000])
ax.set_ylim([0, 180])
current_time = 0
data = pd.DataFrame(columns=range(11))


def init():
    for l in file:
        populate_data(l)
    s = data['e1_8'].dropna()
    line.set_data(s.index, s)


def populate_data(file_line):
    readings = get_readings(file_line)
    current_time = readings['time']

    speed_readings = get_all_detectors_speeds_readings(readings)
    mean_speeds = get_all_detectors_mean_speeds(speed_readings)

    if mean_speeds == {}:
        return

    global data
    data.columns = readings.keys()
    row = pd.DataFrame(mean_speeds, index=[current_time])
    data = pd.concat([data, row])


def on_file_change(arg):
    l = file.readline()
    if not l:
        print('Nothing New')
    else:
        run(l)
        print('Call Function: ', line)


def get_readings(line):
    return eval(line)


def get_all_detectors_mean_speeds(speed_readings):
    mean_speeds = {}
    for id in speed_readings.keys():
        speeds = speed_readings[id]
        if len(speeds) > 0:
            mean_speeds[id] = sum(speeds) / len(speeds)
    return mean_speeds


def get_all_detectors_speeds_readings(readings):
    detector_ids = list(readings.keys())[1:]
    speed_readings = {}
    for id in detector_ids:
        speeds = get_speed_readings(readings[id])
        speed_readings[id] = speeds
    return speed_readings


def get_speed_readings(readings):
    speeds = []
    if isinstance(readings, list):
        for veh_data in readings:
            if veh_data[3] != -1:
                speed = calculate_vehicle_speed(veh_data)
                speeds.append(mps_to_kmh(speed))
    return speeds


def calculate_vehicle_speed(veh_data):
    veh_length = veh_data[1]
    entry_time = veh_data[2]
    exit_time = veh_data[3]
    return veh_length / (exit_time - entry_time)


def mps_to_kmh(speed):
    return speed * 3.6


def run(file_line):
    populate_data(file_line)

    s = data['e1_8'].dropna()
    line.set_data(s.index, s)

    adjust_axis()

    return line,


def adjust_axis():
    xmin, xmax = ax.get_xlim()

    if current_time >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()


ani = animation.FuncAnimation(
    fig,
    on_file_change,
    interval=1000,
    init_func=init)

plt.show()
