import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
import pandas
import csv
import datetime
import itertools
from bokeh.palettes import Dark2_5 as palette

'''
# def replace_tdeg(t_list):
#     return t_list.replace('tdeg=', '')

# df = pandas.read_csv("log.txt")
with open("log.txt", "r") as file:
    data = csv.reader(file, delimiter=" ")

#     # Perform what you need to do on data
#     for row in data:
#         print(row)

    # Can then load into a df if needed
    df = pandas.DataFrame.from_records(data)
    # transform the first row into column indexes
    
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    # getting dataframe only for needed command (which means temperature data)
    temp_frames = df[df.COMMAND == "COMMAND:0x05"]

    # getting a list of ID's with the command above
    devices_list = list(dict.fromkeys(temp_frames['ID'].tolist()))
    # commands_list = list(dict.fromkeys(temp_frames['COMMAND'].tolist()))

    # get the dictionary with the x, y grids values tuple {"ID_key" ([x1,x2,...xn], [y1,y2,...yn])}
    time_series_dict = {}
    for device_id in devices_list:
        tf_device = temp_frames[temp_frames.ID == device_id]
        # get the date and time in string
        time_dev = list(map(lambda a, b: a+' '+b, tf_device['date'].tolist(), tf_device['time'].tolist() ))
        # convert date and time to datetime format
        time_dev = list(map(lambda a: datetime.datetime.strptime(a, '%d.%m.%Y %H:%M:%S'), time_dev) )
        # get the temperature data
        temp_value_dev = tf_device['tdeg'].tolist()
        # cut the crap (tdeg=) from the temperature value
        temp_value_dev = list(map(lambda x: x.replace('tdeg=', ''), temp_value_dev))
        # convert string to integer
        temp_value_dev = [int(i) for i in temp_value_dev] 
        time_series_dict[device_id] = (time_dev, temp_value_dev)
# # Outer temperature data
# with open("out_t.txt", "r") as file:
#     data = csv.reader(file, delimiter="%")
#     df = pandas.DataFrame.from_records(data)
    
#     first_date_m_y = ".11.2015"
#     first_date = "02"+first_date_m_y
    
#     out_temp_list = df.iloc[:, 1].tolist()

#     day_hours = 0
#     date_m = 2   
#     out_timedate_list = []
#     df_time_list = df.iloc[:, 0].tolist()
#     # add date to time list
#     for time_str in df_time_list:
#         # check if it's a new day
#         if int(time_str[0:1]) < day_hours:
#             date_m = date_m + 1
#         day_hours = int(time_str[0:1])
#         out_timedate_list.append(datetime.datetime.strptime(str('{:02}'.format(date_m))+first_date_m_y+" "+time_str, '%d.%m.%Y %H:%M:%S') ) 
# Outer temperature data
with open("out_t-.txt", "r") as file:
    data = csv.reader(file, delimiter=" ")
    df = pandas.DataFrame.from_records(data)
    
    out_temp_list = df.iloc[:, 3].tolist()

    # get the date and time in string
    out_timedate_list = list(map(lambda a, b: a+' '+b, df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist() ))
    # convert date and time to datetime format
    out_timedate_list = list(map(lambda a: datetime.datetime.strptime(a, '%m/%d/%Y %H:%M:%S'), out_timedate_list) )
time_series_dict["out_temp"] = (out_timedate_list, out_temp_list)
# Wood Loads 
with open("loading.txt", "r") as file:
    data = csv.reader(file, delimiter=" ")
    df = pandas.DataFrame.from_records(data)
    
    load_amount_list = df.iloc[:, 3].tolist()

    # get the date and time in string
    load_timedate_list = list(map(lambda a, b: a+' '+b, df.iloc[:, 0].tolist(), df.iloc[:, 1].tolist() ))
    # convert date and time to datetime format
    load_timedate_list = list(map(lambda a: datetime.datetime.strptime(a, '%m/%d/%Y %H:%M'), load_timedate_list) )
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

plot1 = figure(title="Графіки нагріву котла в Каневі", x_axis_type='datetime', tools=TOOLS)

line_colors = itertools.cycle(palette) 

for dev in time_series_dict.keys():
    if dev != "ID:0xF002":
        if dev == "ID:0x3EE0":
            label = "Дверцята х10"
        elif dev == "ID:0x2EE0":
            label = "Кімната"
        elif dev == "ID:0x4EE0":
            label = "Подача"
        elif dev == "ID:0x1EE0":
            label = "Обратка"
        elif dev == "out_temp":
            label = "Вулиця"
        else:
            label = dev
        x, y = time_series_dict[dev]
        if dev == "ID:0x3EE0":
            y = list(map(lambda a: int(a)/10, y ))
        plot1.line(x, y, legend_label=label, color=next(line_colors) )

# source = ColumnDataSource(data=dict(x=load_timedate_list, counts=load_amount_list))
# plot1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="#036564", line_color="#033649")
# plot1.vbar(width=0.9, legend_label="Загрузки", color=next(line_colors), source=source )

plot1.circle(load_timedate_list, load_amount_list, legend_label="Загрузки", color=next(line_colors) )

# plot1.y_range.start = 0
plot1.x_range.range_padding = 0.1
plot1.xaxis.major_label_orientation = 1
# plot1.xgrid.grid_line_color = None

output_file("graph.html", title="heating system log")

# show(gridplot([p1, p2], ncols=2, plot_width=400, plot_height=400))  # open a browser

# show(p2, plot_width=400, plot_height=400)  # open a browser
show(plot1, plot_width=400, plot_height=400)  # open a browser

# TODO: Check and reverse datas (make them follow from left to right)
# TODO: Disable and enable lines

time_series_dict["ID:0x5EE0"]
# temp_frames
devices_list
# commands_list
# time_series_dict
devices_list = list(dict.fromkeys(df['ID'].tolist()))
"""
COMMANDS:
0x05: temperature
0x0B: voltage
"""
commands_list = list(dict.fromkeys(df['COMMAND'].tolist()))
# t1['ID'].tolist()
# devices_list
commands_list

gb = df.groupby('ID')
gb.sum()
df
df[df.ID == "ID:0x9CC0"]
import numpy as np

from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.palettes import Viridis3
from bokeh.plotting import figure
from bokeh.models import CheckboxGroup, CustomJS

output_file("line_on_off.html", title="line_on_off.py example")

p = figure()
props = dict(line_width=4, line_alpha=0.7)
x = np.linspace(0, 4 * np.pi, 100)
l0 = p.line(x, np.sin(x), color=Viridis3[0], legend_label="Line 0", **props)
l1 = p.line(x, 4 * np.cos(x), color=Viridis3[1], legend_label="Line 1", **props)
l2 = p.line(x, np.tan(x), color=Viridis3[2], legend_label="Line 2", **props)

checkbox = CheckboxGroup(labels=["Line 0", "Line 1", "Line 2"],
                         active=[0, 1, 2], width=100)
checkbox.js_on_click(CustomJS(args=dict(l0=l0, l1=l1, l2=l2, checkbox=checkbox),
                            code="""
l0.visible = 0 in checkbox.active;
l1.visible = 1 in checkbox.active;
l2.visible = 2 in checkbox.active;
"""))

layout = row(checkbox, p)
show(layout)
from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import CheckboxGroup, CustomJS

output_file("layout.html")

x = list(range(11))
y0 = x
y1 = [10 - i for i in x]
y2 = [abs(i - 5) for i in x]

s1 = figure(plot_width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)

s2 = figure(plot_width=250, plot_height=250, title=None)
s2.triangle(x, y1, size=10, color="firebrick", alpha=0.5)

s3 = figure(plot_width=250, plot_height=250, title=None)
s3.square(x, y2, size=10, color="olive", alpha=0.5)

col = column(s1, s2, s3)

checkbox = CheckboxGroup(labels=["Plot 1", "Plot 2", "Plot 3"],
                         active=[0, 1, 2], width=100)

callback = CustomJS(args=dict(plots=[s1,s2, s3], col=col, checkbox=checkbox), code="""
const children = []
for (const i of checkbox.active) {
     children.push(plots[i])
} 
col.children = children
""")
checkbox.js_on_change('active', callback)

show(row(checkbox, col))

import numpy as np

from bokeh.io import show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.layouts import column, row

t = np.arange(0.0, 2.0, 0.01)
s = np.sin(3*np.pi*t)
c = np.cos(3*np.pi*t)

source = ColumnDataSource(data=dict(t=t, s=s, c=c))

plot = figure(plot_width=400, plot_height=400)
a = plot.line('t', 's', source=source, line_width=3, line_alpha=0.6, line_color='blue')
b = plot.line('t', 'c', source=source, line_width=3, line_alpha=0.6, line_color='red')

checkbox = CheckboxGroup(labels=["Cosinus", "Sinus"], active=[0,1])

checkbox.js_on_click(CustomJS(args=dict(line0=a, line1=b), code="""
    //console.log(cb_obj.active);
    line0.visible = false;
    line1.visible = false;
    for (i in cb_obj.active) {
        //console.log(cb_obj.active[i]);
        if (cb_obj.active[i] == 0) {
            line0.visible = true;
        } else if (cb_obj.active[i] == 1) {
            line1.visible = true;
        }
    }
""") )

layout = row(plot, widgetbox(checkbox))

show(layout)
'''