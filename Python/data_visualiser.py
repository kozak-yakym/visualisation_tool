import csv
import datetime
import itertools
import os
import re

import numpy as np
import pandas as pd

from bokeh.io import output_file, show
from bokeh.layouts import column, row  # , gridplot, widgetbox
from bokeh.models import CheckboxGroup, ColumnDataSource, CustomJS
from bokeh.palettes import Dark2_5 as palette, Viridis3
from bokeh.plotting import figure

DATASET_PATH = "..\\dataset\\"

log_path = os.path.abspath(os.path.join(
    __file__, DATASET_PATH, 'log.txt'))
out_t_path = os.path.abspath(os.path.join(
    __file__, DATASET_PATH, 'out_t-.txt'))
loading_path = os.path.abspath(os.path.join(
    __file__, DATASET_PATH, 'loading.txt'))


# Main log data
with open(log_path, "r") as file:
    data = csv.reader(file, delimiter=" ")

    # Can then load into a df if needed.
    df = pd.DataFrame.from_records(data)

    # Transform the first row into column indexes.
    new_header = df.iloc[0]  # Grab the first row for the header.
    df = df[1:]  # Take the data less the header row.
    df.columns = new_header  # Set the header row as the df header.

    # Getting dataframe only for needed command (which means temperature data).
    temp_frames = df[df.COMMAND == "COMMAND:0x05"]

    # Getting a list of ID's with the command above.
    devices_list = list(dict.fromkeys(temp_frames['ID'].tolist()))
    # Commands_list = list(dict.fromkeys(temp_frames['COMMAND'].tolist())).

    # Get the dictionary with the x, y grids values tuple {"ID_key" ([x1,x2,...xn], [y1,y2,...yn])}.
    time_series_dict = {}
    for device_id in devices_list:
        tf_device = temp_frames[temp_frames.ID == device_id]
        # Get the date and time in string.
        time_dev = list(map(lambda a, b: a+' '+b,
                        tf_device['date'].tolist(), tf_device['time'].tolist()))
        # Convert date and time to datetime format.
        time_dev = list(map(lambda a: datetime.datetime.strptime(
            a, '%d.%m.%Y %H:%M:%S'), time_dev))
        # Get the temperature data.
        temp_value_dev = tf_device['tdeg'].tolist()
        # Cut the crap (tdeg=) from the temperature value.
        temp_value_dev = list(
            map(lambda x: x.replace('tdeg=', ''), temp_value_dev))
        # Convert string to integer.
        temp_value_dev = [int(i) for i in temp_value_dev]
        time_series_dict[device_id] = (time_dev, temp_value_dev)

# Outer temperature data
with open(out_t_path, "r") as file:
    data = csv.reader(file, delimiter=" ")
    df = pd.DataFrame.from_records(data)

    out_temp_list = df.iloc[:, 3].tolist()

    # get the date and time in string
    out_timedate_list = list(
        map(lambda a, b: a+' '+b, df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()))
    # convert date and time to datetime format
    out_timedate_list = list(map(lambda a: datetime.datetime.strptime(
        a, '%m/%d/%Y %H:%M:%S'), out_timedate_list))
time_series_dict["out_temp"] = (out_timedate_list, out_temp_list)

# Boiler Loadings
with open(loading_path, "r") as file:
    data = csv.reader(file, delimiter=" ")
    df = pd.DataFrame.from_records(data)

    load_amount_list = df.iloc[:, 3].tolist()

    # get the date and time in string
    load_timedate_list = list(
        map(lambda a, b: a+' '+b, df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist()))
    # convert date and time to datetime format
    load_timedate_list = list(map(lambda a: datetime.datetime.strptime(
        a, '%m/%d/%Y %H:%M'), load_timedate_list))
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

plot1 = figure(title="Graphs from the heating system sensors.",
               x_axis_type='datetime', tools=TOOLS)

line_colors = itertools.cycle(palette)

for dev in time_series_dict.keys():
    if dev != "ID:0xF002":
        if dev == "ID:0x3EE0":
            label = "Door, t°C х10"
        elif dev == "ID:0x2EE0":
            label = "Room, t°C"
        elif dev == "ID:0x4EE0":
            label = "Feed, t°C"
        elif dev == "ID:0x1EE0":
            label = "Return, t°C"
        elif dev == "out_temp":
            label = "Outside, t°C"
        else:
            label = dev
        x, y = time_series_dict[dev]
        if dev == "ID:0x3EE0":
            y = list(map(lambda a: int(a)/10, y))
        plot1.line(x, y, legend_label=label, color=next(line_colors))

plot1.circle(load_timedate_list, load_amount_list,
             legend_label="Loads, RefVol.", color=next(line_colors))

# plot1.y_range.start = 0
plot1.x_range.range_padding = 0.1
plot1.xaxis.major_label_orientation = 1
# plot1.xgrid.grid_line_color = None

output_file("graph.html", title="heating system log")

show(plot1, plot_width=800, plot_height=400)  # open a browser
