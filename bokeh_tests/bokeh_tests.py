import time
import json
import urllib.request
import datetime
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import HoverTool, LayoutDOM, NumeralTickFormatter, DatetimeTickFormatter

symbol = "AAPL"
time_scale = "daily"  # daily, weekly, monthly


# """This commented out data for getting actual time series"""
# start = time.time()
# url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{time_scale.upper()}&symbol={symbol}&apikey=1PSE4E7QME3PUPTU"
# webpage = urllib.request.urlopen(url)
# data = json.loads(webpage.read().decode())
# print(time.time() - start)
#
# if time_scale == "daily":
#     time_points = data['Time Series (Daily)']
# elif time_scale == "weekly":
#     time_points = data['Weekly Time Series']
# elif time_scale == "monthly":
#     time_points = data['Monthly Time Series']
#
# total_data = []
# dates = []
# prices = []
# volumes = []
# for point in time_points:
#     date = point.split('-')
#     dates.append(datetime.date(int(date[0]), int(date[1]), int(date[2])))
#     prices.append(float(time_points[point]['4. close']))
#     volumes.append(int(time_points[point]['5. volume']))
#     total_data.append((point, float(time_points[point]['4. close']), int(time_points[point]['5. volume'])))
#
# """This commented out data for making json txt file for quick loading"""
# f = open(f'{symbol}_stock_{time_scale}.txt', 'w')
# json.dump(total_data, f)
# f.close()


"""This section for opening and getting data from json txt file"""
f = open(f'{symbol}_stock_{time_scale}.txt', 'r')
x = json.load(f)
total_data = []
dates = []
prices = []
volumes = []
for point in x:
    date = point[0].split('-')
    dates.append(datetime.date(int(date[0]), int(date[1]), int(date[2])))
    prices.append(point[1])
    volumes.append(point[2])
    print(date, point[1], point[2])
"""end get data from json txt file"""


# Source data
source = ColumnDataSource(data=dict(
    dates=dates,
    prices=prices,
    volumes=volumes
))


# output to static HTML file
output_file("stock_test.html")

TOOLS = "pan, wheel_zoom, save, reset"

hover = HoverTool(
    tooltips=[
        ('date',   '@dates{%F}'),
        ('price',  '$@{prices}{%0.2f}'),  # use @{ } for field names with spaces
        ('volume', '@volumes{0.00 a}'),
    ],

    formatters={
        'dates': 'datetime',  # use 'datetime' formatter for 'dates' field
        'prices': 'printf',   # use 'printf' formatter for 'prices' field
                              # use default 'numeral' formatter for other fields
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline',
)

if time_scale == "daily":
    time_title = "Day"
elif time_scale == "weekly":
    time_title = "Week"
elif time_scale == "monthly":
    time_title = "Month"

# create a new plot with a title and axis labels
p = figure(title=f"{symbol} Prices by {time_title}",
           x_axis_label='Dates',
           y_axis_label='Price',
           x_axis_type="datetime",
           plot_width=800,
           plot_height=400,
           tools=[hover, TOOLS],
           active_scroll="wheel_zoom",
           sizing_mode="scale_width",
           )

# Border commands
p.border_fill_color = '#bfff00'

# Outline commands
p.outline_line_color = 'black'
p.outline_line_width = 1

# Set background color
p.background_fill_color = '#4a7d66'

# Set title controls
p.title.text_color = '#cb9a01'

# Axis line controls
p.axis.axis_line_width = 3
p.axis.minor_tick_in = -2
p.axis.minor_tick_out = 8
p.axis.major_tick_out = 10
p.axis.minor_tick_in = -2
p.axis.minor_tick_out = 6
p.axis.axis_label_text_color = "#000099"
p.axis.axis_label_standoff = 30
p.axis.axis_label_text_font_style = 'bold'

# Grid controls
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_color = '#cb9a01'

# Create flexible date formatter
time_delta = (dates[0] - dates[len(dates)-1]).days
if time_delta >= 365*2:
    date_format = "%Y"
elif 90 < time_delta < 365*2:
    date_format = "%m/%Y"
else:
    date_format = "%m/%d%"

# Axis formatters
p.xaxis.formatter = DatetimeTickFormatter(months=date_format)
p.yaxis.formatter = NumeralTickFormatter(format="$0.00")


# add a line renderer with legend and line thickness
p.line(  # dates, prices,
       x='dates', y='prices',
       legend=False,
       line_width=2,
       line_color='#cb9a01',
       line_cap='round',
       source=source)

# # Legend (only usable after render data declared)
# p.legend.visible = False


# show the results
show(p)

