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
from urllib.error import HTTPError
import calendar


def bokeh_graph(symbol, time_frame):
    # Assumes average month = 22 working days
    if time_frame == '1 month':
        time_interval = "daily"
        max_points = 22
    elif time_frame == '3 month':
        time_interval = "daily"
        max_points = 22 * 3
    elif time_frame == '1 year':
        time_interval = "weekly"
        max_points = 53
    elif time_frame == '5 year':
        time_interval = "weekly"
        max_points = 52 * 5 + 2
    elif time_frame == '20 year':
        time_interval = "monthly"
        max_points = 12 * 20 + 1
    else:
        return "Invalid time frame format", None

    name, json_data = search_json(symbol, time_interval)

    # If search_json worked
    if name and json_data:
        x = json.loads(json_data)
        dates = []
        prices = []
        volumes = []
        counter = 0
        for point in x:
            date = point[0].split('-')
            dates.append(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            prices.append(point[1])
            volumes.append(point[2])
            counter += 1
            if counter == max_points:
                break

        # Source data
        source = ColumnDataSource(data=dict(
            dates=dates,
            prices=prices,
            volumes=volumes
        ))

        # output to static HTML file
        # output_file("stock_test.html")

        TOOLS = "pan, wheel_zoom, save, reset"

        hover = HoverTool(
            tooltips=[
                ('date',   '@dates{%D}'),
                ('price',  '$@prices{%0.2f}'),
                ('volume', '@volumes{0.00 a}'),
            ],

            formatters={
                'dates': 'datetime',  # use 'datetime' formatter for 'dates' field
                'prices': 'printf',   # use 'printf' formatter for 'prices' field
                                      # use default 'numeral' formatter for others
            },

            # display a tooltip whenever the cursor is vertically in line with data
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
                   active_drag=None,
                   active_scroll=None,
                   sizing_mode="scale_width",
                   )

        # Border commands
        p.border_fill_color = '#EBE8BE'

        # Outline commands
        p.outline_line_color = '#083836'
        p.outline_line_width = 1

        # Set background color
        p.background_fill_color = '#B3C87A'

        # Set title controls
        p.title.text_color = '#202E24'

        # Axis line controls
        p.axis.axis_line_width = 3
        p.axis.minor_tick_in = -2
        p.axis.minor_tick_out = 8
        p.axis.major_tick_out = 10
        p.axis.minor_tick_in = -2
        p.axis.minor_tick_out = 6
        p.axis.axis_label_text_color = "#202E24"
        p.axis.axis_label_standoff = 10
        p.axis.axis_label_text_font_style = 'bold'

        # Grid controls
        p.grid.grid_line_alpha = 0.3
        p.grid.grid_line_color = '#202E24'

        # Create flexible date formatter
        time_delta = (dates[0] - dates[len(dates)-1]).days

        years_format =  "%Y"
        months_format = "%m/%Y"
        days_format =   "%m/%d/%Y"

        # Axis formatters
        p.xaxis.formatter = DatetimeTickFormatter(
            days=days_format, months=months_format, years=years_format)
        p.yaxis.formatter = NumeralTickFormatter(format="$0.00")


        # add a line renderer with legend and line thickness
        p.line(  # dates, prices,
               x='dates', y='prices',
               legend=False,
               line_width=2,
               line_color='#202E24',
               line_cap='round',
               source=source)

        # # Legend (only usable after render data declared)
        # p.legend.visible = False


        # # show the results
        # show(p)

        script, div = components(p)
        return script, div
    # If search_json didn't work, either time interval wrong or no stock found
    else:
        return "No stock found!", None


def search_json(symbol, time_interval):
    # Get stock info from stock's symbol
    try:
        stock = StockInfo.objects.get(symbol__exact=symbol)
    except ObjectDoesNotExist:
        print("stock not found...")
        return "stock not found", None
    try:
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        # Use update time and json_points for specific interval
        if time_interval == "daily":
            update_datetime = stock.day_json_update_time
            json_points = stock.day_json
            # If before market close
            if now.hour < 21:
                # check against yesterday close
                check_day = now - datetime.timedelta(days=1)
            # After market open
            else:
                # check against today's close
                check_day = now
            # check against market close
            check_datetime = check_day.replace(hour=21, minute=0, second=0,
                                               microsecond=0)
        elif time_interval == "weekly":
            update_datetime = stock.week_json_update_time
            json_points = stock.week_json
            # Check if updated within past 7 days
            check_datetime = now - datetime.timedelta(days=7)
        elif time_interval == "monthly":
            update_datetime = stock.month_json_update_time
            json_points = stock.month_json
            # Check if updated this month
            check_datetime = now.replace(day=1)
        else:
            return "Invalid time interval", None
    except AttributeError:
        print("time interval not found...")
        return "Time interval not found...", None

    # Check if stock is found in database. All stocks from
    # (http://www.nasdaq.com/screening/company-list.aspx) should exist
    if stock:
        # Check if stock json_points was ever updated in database
        if json_points and update_datetime:
            # Check if json was updated recently
            # If not updated recently, then update
            if update_datetime < check_datetime:
                json_points = update_json(stock, time_interval)
            # Stock was recently updated (no new update necessary)
            else:
                pass
        # Stock price never updated in database, update it now
        else:
            json_points = update_json(stock, time_interval)

        # Store current json_data and names as variables
        name = stock.name
        json_data = json_points

    # Stock wasn't found in database, return no price or name
    else:
        name = "Stock not found!"
        json_data = None

    return name, json_data


def update_json(stock, time_interval):
    # Time our api call
    start = time.time()
    # Load json from api call
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{time_interval.upper()}&symbol={stock.symbol}&apikey=1PSE4E7QME3PUPTU"
    try:
        webpage = urllib.request.urlopen(url)
    except HTTPError:
        print("Graph loading timed out, please try again.")
        return None
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
    for point in time_points:
        total_data.append((point, float(time_points[point]['4. close']),
                           int(time_points[point]['5. volume'])))

    # Get current time
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if time_interval == "daily":
        stock.day_json = json.dumps(total_data)
        stock.day_json_update_time = now
        try:
            stock.save()
            return stock.day_json
        except:
            return None

    elif time_interval == "weekly":
        stock.week_json = json.dumps(total_data)
        stock.week_json_update_time = now
        try:
            stock.save()
            return stock.week_json
        except:
            return None
    elif time_interval == "monthly":
        stock.month_json = json.dumps(total_data)
        stock.month_json_update_time = now
        try:
            stock.save()
            return stock.month_json
        except:
            return None

    else:
        return None


if __name__ == "__main__":

    stock_symbol = "MSFT"
    stock_time_interval = "daily"  # daily, weekly, monthly

    bokeh_graph(stock_symbol, stock_time_interval)
