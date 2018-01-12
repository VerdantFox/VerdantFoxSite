import time
import json
import urllib.request
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, NumeralTickFormatter, DatetimeTickFormatter
from bokeh.embed import components
from .models import StockInfo
from django.core.exceptions import ObjectDoesNotExist


def bokeh_graph(symbol, time_interval):

    """This commented out data for getting actual time series"""
    start = time.time()
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{time_interval.upper()}&symbol={symbol}&apikey=1PSE4E7QME3PUPTU"
    webpage = urllib.request.urlopen(url)
    data = json.loads(webpage.read().decode())
    print(time.time() - start)

    if time_interval == "daily":
        time_points = data['Time Series (Daily)']
    elif time_interval == "weekly":
        time_points = data['Weekly Time Series']
    elif time_interval == "monthly":
        time_points = data['Monthly Time Series']
    else:
        time_points = data['Time Series (Daily)']

    total_data = []
    dates = []
    prices = []
    volumes = []
    for point in time_points:
        date = point.split('-')
        dates.append(datetime.date(int(date[0]), int(date[1]), int(date[2])))
        prices.append(float(time_points[point]['4. close']))
        volumes.append(int(time_points[point]['5. volume']))
        total_data.append((point, float(time_points[point]['4. close']), int(time_points[point]['5. volume'])))

    """This commented out data for making json txt file for quick loading"""
    f = open(f'{symbol}_stock_{time_interval}.txt', 'w')
    json.dump(total_data, f)
    f.close()


    """This section for opening and getting data from json txt file"""
    f = open(f'Finance/{symbol}_stock_{time_interval}.txt', 'r')
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
        # print(date, point[1], point[2])
    """end get data from json txt file"""


    # Source data
    source = ColumnDataSource(data=dict(
        dates=dates,
        prices=prices,
        volumes=volumes
    ))


    # # output to static HTML file
    # output_file("stock_test.html")

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

    if time_interval == "daily":
        time_title = "Daily"
    elif time_interval == "weekly":
        time_title = "Weekly"
    elif time_interval == "monthly":
        time_title = "Monthly"

    # create a new plot with a title and axis labels
    p = figure(title=f"{symbol} {time_title} Stock Prices",
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
    p.axis.axis_label_standoff = 10
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


    # # show the results
    # show(p)

    script, div = components(p)
    print(script)
    print("**********************************")
    print(div)
    return script, div


def search_stock_graph(symbol, time_interval):

    # Get stock info from stock's symbol
    try:
        stock = StockInfo.objects.get(symbol__exact=symbol)
    except ObjectDoesNotExist:
        print("stock not found...")
        stock = None

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    # Use update time and json_points for specific interval
    if time_interval == "daily":
        update_time = stock.day_json_update_time
        json_points = stock.day_json
        check_datetime = now.replace(hour=14, minute=0, second=0, microsecond=0)
    elif time_interval == "weekly":
        update_time = stock.week_json_update_time
        json_points = stock.week_json
        check_datetime = now.replace(day=1)
    elif time_interval == "monthly":
        update_time = stock.month_json_update_time
        json_points = stock.month_json
        check_datetime = now.replace(day=1)
    else:
        print('invalid time_interval: using daily instead')
        update_time = stock.day_json_update_time
        json_points = stock.day_json
        check_datetime = now.replace(hour=14, minute=0, second=0, microsecond=0)

    # Check if stock is found in database. All stocks from
    # (http://www.nasdaq.com/screening/company-list.aspx) should exist
    if stock:
        # Check if stock json_points was ever updated in database
        if json_points and update_time:
            # Check if json was updated recently
            # If not updated recently, then update
            if update_time < check_datetime:
                pass

            # Stock was recently updated (no new update necessary)
            else:
                pass
        # Stock price never updated in database, update it now
        else:
            pass

        # Store current json_data and names as variables
        name = stock.name
        json_data = json_points

    # Stock wasn't found in database, return no price or name
    else:
        name = None
        json_data = None

    return name, json_data


def update_json_data(stock, time_interval):
    # Time our api call
    start = time.time()
    # Load json from api call
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{time_interval.upper()}&symbol={stock.symbol}&apikey=1PSE4E7QME3PUPTU"
    webpage = urllib.request.urlopen(url)
    data = json.loads(webpage.read().decode())
    print(f"{time_interval.upper()} api call time:", time.time() - start)

    if time_interval == "daily":
        time_points = data['Time Series (Daily)']
    elif time_interval == "weekly":
        time_points = data['Weekly Time Series']
    elif time_interval == "monthly":
        time_points = data['Monthly Time Series']
    else:
        print("error updating_json_interval")
        return None

    total_data = []
    dates = []
    prices = []
    volumes = []
    for point in time_points:
        date = point.split('-')
        dates.append(datetime.date(int(date[0]), int(date[1]), int(date[2])))
        prices.append(float(time_points[point]['4. close']))
        volumes.append(int(time_points[point]['5. volume']))
        total_data.append((point, float(time_points[point]['4. close']), int(time_points[point]['5. volume'])))

    if time_interval == "daily":
        time_points = data['Time Series (Daily)']
    elif time_interval == "weekly":
        time_points = data['Weekly Time Series']
    elif time_interval == "monthly":
        time_points = data['Monthly Time Series']

    json.dump(total_data, f)


if __name__ == "__main__":

    stock_symbol = "MSFT"
    stock_time_interval = "daily"  # daily, weekly, monthly

    bokeh_graph(stock_symbol, stock_time_interval)