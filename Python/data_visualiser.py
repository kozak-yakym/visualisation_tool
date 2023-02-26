import csv
import datetime
import itertools
import os
import re

import numpy as np
import pandas as pd

from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.models import CheckboxGroup, ColumnDataSource, CustomJS, Legend, Div
from bokeh.palettes import Dark2_5 as palette, Viridis3
from bokeh.plotting import figure
from itertools import cycle

DATASET_PATH = "dataset"

log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATASET_PATH, 'log.txt')
out_t_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATASET_PATH, 'out_t-.txt')
loading_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATASET_PATH, 'loading.txt')

def parse_csv_to_df(file_path, skip_rows=0):
    with open(file_path, "r") as file:
        data = csv.reader(file, delimiter=" ")

        # Convert data to a DataFrame.
        df = pd.DataFrame.from_records(data)

        # Set the first row as the column names.
        new_header = df.iloc[0] 
        df = df[1:] 
        df.columns = new_header 

        # Return the DataFrame.
        return df.iloc[skip_rows:]

# Load the Main log data.
log_df = parse_csv_to_df(log_path)

# Load the outside temperature data.
out_t_df = parse_csv_to_df(out_t_path)

# Load the Boiler loading data.
load_df = parse_csv_to_df(loading_path)


# ==================Main log data processing==================
# TODO: Move to the function.
# Get a DataFrame with only the temperature data.
temp_frames = log_df[log_df.COMMAND == "COMMAND:0x05"]

# Get a list of unique device IDs with temperature data.
devices_list = temp_frames['ID'].unique().tolist()

# Get the time series data for each device.
time_series_dict = {}
for device_id in devices_list:
    tf_device = temp_frames[temp_frames.ID == device_id]

    # Get the date and time in datetime format.
    time_dev = pd.to_datetime(tf_device['date'] + ' ' + tf_device['time'], format='%d.%m.%Y %H:%M:%S')

    # Get the temperature data.
    temp_value_dev = tf_device['tdeg'].str.replace('tdeg=', '').astype(int)

    # Store the time series data for this device in the dictionary.
    time_series_dict[device_id] = (time_dev, temp_value_dev)

# =============Outer temperature data processing==============
# TODO: Move to the function.
# Convert the date and time to datetime format.
out_timedate = pd.to_datetime(out_t_df.iloc[:, 0] + ' ' + out_t_df.iloc[:, 1], format='%m/%d/%Y %H:%M:%S')

# Get the outside temperature data.
out_temp = out_t_df.iloc[:, 3].astype(float)

# Add the values to time_series_dict[].
time_series_dict["out_temp"] = (out_timedate, out_temp)

# =================Boiler Loadings processing=================
# Load the boiler loading data.
load_amount = load_df.iloc[:, 3].astype(float)

# Convert the date and time to datetime format.
load_timedate = pd.to_datetime(load_df.iloc[:, 0] + ' ' + load_df.iloc[:, 1], format='%m/%d/%Y %H:%M')



# ========================Draw graphs=========================
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

plot1 = figure(title="Graphs from the heating system sensors.",
               x_axis_type='datetime', tools=TOOLS)

line_colors = cycle(palette)

legend_items = []
for dev, values in time_series_dict.items():
    if dev == "ID:0xF002":
        continue  # Skip this device.
    elif dev == "ID:0x5EE0":
        continue  # Skip this device too.
    elif dev == "ID:0x3EE0":
        label = "Door, t°C × 10"
        values = values[0], list(map(lambda a: int(a)/10, values[1]))
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
    x, y = values
    line = plot1.line(x, y, color=next(line_colors))
    legend_items.append((label, [line]))

load_line = plot1.circle(load_timedate, load_amount,
                         color=next(line_colors))

legend_items.append(("Loads, RefVol.", [load_line]))

legend = Legend(items=legend_items)
plot1.add_layout(legend, 'right')

checkbox_group = CheckboxGroup(labels=[label for label, _ in legend_items], active=list(range(len(legend_items))))
checkbox_group.js_on_change('active', CustomJS(args=dict(legend=legend), code="""
    var items = legend.items;
    for (var i = 0; i < items.length; i++) {
        items[i].renderers[0].visible = cb_obj.active.includes(i);
    }
    legend.location = "right";
"""))

# Create Div, which uses JavaScript.
js = CustomJS(args=dict(p=plot1), code="""
    function resize() {
        p.plot_width = window.innerWidth - 100;
    }
    window.addEventListener('resize', resize);
    resize();
""")
div = Div()
div.js_on_change('text', js)

layout = row(div, checkbox_group, plot1)
output_file("graph.html", title="heating system log")

show(layout)  # Open a browser.