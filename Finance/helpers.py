import urllib.request
from urllib.error import HTTPError
import json
from .models import Transaction, StockInfo
import time
from django.contrib import messages
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def search_stock_info(symbol):
    try:
        stock = StockInfo.objects.get(symbol__exact=symbol)
    except ObjectDoesNotExist:
        stock = None

    # Check if stock is found in database. All stocks from
    # (http://www.nasdaq.com/screening/company-list.aspx) should exist
    if stock:
        # Check if stock recently updated
        recent = check_price_updated(stock, stock.price_update_time)
        if recent:
            # Use current stock price
            pass
        else:
            update_stock_price(stock)

        # Store current stock price and names as variables
        current_price = stock.price
        name = stock.name

    # Stock wasn't found in database, return no price or name
    else:
        name = None
        current_price = None

    return name, current_price


def update_stock_price(stock):
    # Look up stock price
    price = single_lookup(stock.symbol)
    # Update stock info with current price
    stock.price = price
    # Update stock with current datetime (UTC)
    stock.price_update_time = datetime.datetime.now(tz=datetime.timezone.utc)
    # Save updated stock attributes to database
    stock.save()


def multiple_lookup(symbols):
    """Look up quotes for multiple stock symbols.

    Note: stocks that don't exist will be skipped without error.
    """
    query = ''
    stock_dict = dict()
    symbol_set = set()

    # Add items to set to remove duplicates
    for symbol in symbols:
        symbol_set.add(symbol)

    # Create query string of symbols
    for symbol in symbol_set:
        # Print error for symbols with obvious problems.
        if not symbol.isalpha():
            print(f"error with '{symbol}' symbol alpha during lookup")
        if not 0 < len(symbol) < 6:
            print(f"error with '{symbol}' symbol length during lookup")
        # Add symbol to the set
        query += symbol.upper() + ','

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:
        start_time = time.time()
        # GET JSON webpage
        url = f"https://www.alphavantage.co/query?function=BATCH_STOCK_" \
                  f"QUOTES&symbols={query}&apikey=1PSE4E7QME3PUPTU"

        # Convert JSON data from webpage into readable format
        # https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        try:
            webpage = urllib.request.urlopen(url)
            data = json.loads(webpage.read().decode())
        except HTTPError:
            return "Error: took too long to get stock data, try again."
        print(f"Time = {time.time() - start_time}")
        # Get the stock symbol and it's associated price
        for stock_info in data['Stock Quotes']:
            # Get symbol
            stock_symbol = stock_info['1. symbol']
            # Get symbol and string format it to have 2 decimal places
            stock_price = f"{float(stock_info['2. price']):.2f}"
            # Convert string formatted stock to a float
            stock_price = float(stock_price)
            # Add stock to stock_dict
            stock_dict[stock_symbol] = stock_price

        return stock_dict

    except:
        return "error getting or reading webpage"


def single_lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol with obvious problem
    if not symbol.isalpha() or not 0 < len(symbol) < 6:
        return "Error, not a valid stock symbol"

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:
        start_time = time.time()
        # GET JSON webpage
        url = f"https://www.alphavantage.co/query?function=BATCH_STOCK_" \
                  f"QUOTES&symbols={symbol}&apikey=1PSE4E7QME3PUPTU"

        # Convert JSON data from webpage into readable format
        # https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        webpage = urllib.request.urlopen(url)

        print(f"Time = {time.time() - start_time}")
        data = json.loads(webpage.read().decode())
        # Get the stock symbol and it's associated price

        if data['Stock Quotes'] == []:
            return "Error, stock not found."
        else:
            for stock_info in data['Stock Quotes']:
                stock_price = f"{float(stock_info['2. price']):.2f}"
                stock_price = float(stock_price)
                return stock_price

    except:
        return "Error getting or reading web page."


def stock_index(user):
    """Given a user, return list of unique stocks and total shares"""

    # Query database for UNIQUE stock symbols in "portfolio" from current user
    unique_stocks = Transaction.objects.values('symbol').distinct().filter(user__exact=user)

    # Return empty list if user has no stocks
    if not unique_stocks:
        return []

    # Query database for ALL info in "portfolio" from current user
    stock_portfolio = Transaction.objects.filter(user__exact=user)

    # Make a list to sort unique stock symbols
    presorted_stock_symbol_list = []
    # Iterate over unique stocks, converting each dict to a "symbol" string
    # and appending to presorted stock list
    for stock in unique_stocks:
        presorted_stock_symbol_list.append(stock["symbol"])
    # If "Cash added" is in our list, remove it from our list
    if "FUNDS ADDED" in presorted_stock_symbol_list:
        presorted_stock_symbol_list.remove("FUNDS ADDED")
    # Sort the list of stock symbols
    sorted_stock_symbol_list = sorted(presorted_stock_symbol_list)

    # Create Q object for complex lookup
    q = Q()
    # Add stock names to "OR" = "|" query filter
    for symbol in sorted_stock_symbol_list:
        q |= Q(symbol=symbol)
    # query for user's unique stocks using Q() filter
    db_stocks = StockInfo.objects.filter(q)

    # get current time
    time_now = datetime.datetime.now(tz=datetime.timezone.utc)

    # Create bool variable for checking if ALL user's stock prices are updated
    all_stocks_updated = True

    # Create dictionary of stocks and their updated values
    current_stock_prices = {}

    # Check if all stocks have been updated recently
    for stock in db_stocks:
        # Check if recently updated
        recent = check_price_updated(stock, stock.price_update_time)
        if recent:
            current_stock_prices[stock.symbol] = stock.price
        else:
            all_stocks_updated = False
            break

    if not all_stocks_updated:
        # Look up all current stock prices
        current_stock_prices = multiple_lookup(sorted_stock_symbol_list)
        if isinstance(current_stock_prices, str):
            return current_stock_prices
        # Update all stock prices in db
        for stock in db_stocks:
            stock.price = current_stock_prices[stock.symbol]
            stock.price_update_time = time_now
            stock.save()

    # Create a list of dictionaries where the dictionary keys are:
    # "sybmol", "name", "shares", "price", "total"
    # for each unique stock in list.
    stock_list = []

    # Iterate over sorted, unique stock symbols
    for unique_symbol in sorted_stock_symbol_list:
        # Set "unique_stock_shares" variable to 0 for each unique stock
        unique_stock_shares = 0
        # Iterate over stocks portfolio of current user
        stock_name = ''
        for stock in stock_portfolio:
            # Gives number of shares for each stock by adding each repeated
            # stock shares value to current unique stock

            if stock.symbol == unique_symbol:
                unique_stock_shares += int(stock.shares)
                stock_name = stock.name

        # Get current unique stock value from dict
        stock_price = float(current_stock_prices[unique_symbol])
        # Get total price of all shares for unique stock
        stock_total = stock_price * unique_stock_shares
        # Only update stock_list if user owns stocks
        if stock_total > 0:
            # Append dictionary to stock list with all known info about stock
            stock_list.append(
                {"symbol": unique_symbol,
                 "name": stock_name,
                 "shares": unique_stock_shares,
                 "price": stock_price,
                 "total": stock_total
                 })

    return stock_list


def check_price_updated(stock, update_datetime):
    """Return True if stock updated within 1 hour of most recent market hour
    Else return False"""
    if stock.price and stock.price_update_time:
        # Check if stock price was updated recently (1 hour)
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # Time since stock updated
        time_delta = now - update_datetime
        # Stock market open and closing times
        market_open = now.replace(hour=14, minute=30, second=0,
                                  microsecond=0)
        market_close = now.replace(hour=21, minute=0, second=0,
                                   microsecond=0)
        # day stock updated
        update_date = update_datetime.date()
        # Today and yesterday as dates
        today = now.date()
        yesterday = now.date() - datetime.timedelta(days=1)

        # if during market hours
        if market_open < now < market_close:
            # If updated within last hour
            if time_delta < datetime.timedelta(hours=1):
                # use current price
                return True
            # Not updated within last hour
            else:
                return False
        # Current time is before market hours
        elif now < market_open:
            # If updated today
            if update_date == today:
                return True
            # if updated yesterday after market hours
            elif update_date == yesterday and \
                    update_datetime.time() > market_close.time():
                return True
            # Updated prior to yesterday's market close
            else:
                return False
        # Current time is after market hours
        else:
            # if updated today after market hours
            if update_datetime > market_close:
                return True
            # updated before today's after market hours
            else:
                return False
    # Stock price never updated in database
    else:
        return False


def validate_shares(request, stock_symbol, trans_shares, owned_shares=None):
    try:
        # Invalidate any non-integer
        trans_shares = int(trans_shares)
        # Invalidate any integer less than one or greater than 10000
        if not 0 < trans_shares < 1000:
            messages.add_message(
                request, messages.WARNING,
                f'Failed {stock_symbol} validation, '
                f'shares out of range (1-1000)!',
                extra_tags=' stock'
            )
            return False
        # If selling
        if owned_shares:
            # Invalidate instances where selling more shares than owned
            if trans_shares > owned_shares:
                messages.add_message(
                    request, messages.WARNING,
                    f'Failed {stock_symbol} validation, '
                    f'selling more than owned!',
                    extra_tags=' stock'
                )
                return False
            else:
                # Everything checks out (selling)
                return trans_shares
        else:
            # Everything checks out (buying)
            return trans_shares
    # Catch non-integer or other weird, un-checked-for error
    except:
        messages.add_message(
            request, messages.WARNING,
            f'Failed {stock_symbol} validation, '
            f'Given non-integer share count!',
            extra_tags=' stock'
        )
        return False


def check_repeats(post):
    repeat_symbol_check = ''
    repeat_list = []
    for item in post:
        # Check if item name starts with "buy"
        if item[:3] == "buy":
            # Check if item was bought bought
            if post[item]:
                # Split item to get buy/sell:0 and stock symbol:1
                split_item = item.split('-')
                # Get stock symbol
                # and a copy for checking buying and selling at same time
                repeat_symbol_check = split_item[1]
        # Check if item name starts with "sell"
        if item[:4] == "sell":
            # Check if item was sold
            if post[item]:
                # Check for buying and selling at same time
                split_item = item.split('-')
                stock_symbol = split_item[1]
                if repeat_symbol_check == stock_symbol:
                    repeat_list.append(stock_symbol)
    return repeat_list


if __name__ == "__main__":
    pass
