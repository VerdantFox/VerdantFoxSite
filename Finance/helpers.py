import urllib.request
import json
from .models import Transaction, StockSymbolName
import time
from django.contrib import messages


def get_stock_name(symbol):
    stock = StockSymbolName.objects.values('stock_name').get(
        stock_symbol__exact=symbol)
    stock_name = stock['stock_name']
    return stock_name


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
        webpage = urllib.request.urlopen(url)
        data = json.loads(webpage.read().decode())
        print(f"Time = {time.time() - start_time}")
        # Get the stock symbol and it's associated price
        for stock_info in data['Stock Quotes']:
            stock_symbol = stock_info['1. symbol']
            stock_price = f"{float(stock_info['2. price']):.2f}"
            stock_price = float(stock_price)
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

    # Query database for unique stock symbols in "portfolio" from current user
    unique_stocks = Transaction.objects.values('symbol').distinct().filter(user__exact=user)
    print(unique_stocks)

    # Query database for all info in "portfolio" from current user
    stock_portfolio = Transaction.objects.filter(user__exact=user)

    # Make a list to sort unique stocks
    presorted_stock_list = []
    # Iterate over unique stocks, converting each dict to a single string
    for stock in unique_stocks:
        presorted_stock_list.append(stock["symbol"])
    # If "Cash added" is in our list, remove it from our list
    if "FUNDS ADDED" in presorted_stock_list:
        presorted_stock_list.remove("FUNDS ADDED")
    # Sort the list of stocks (now strings)
    sorted_stock_list = sorted(presorted_stock_list)

    # Create a list of dictionaries where the dictionary keys are:
    # "sybmol", "name", "shares", "price", "total"
    # for each unique stock in list.
    stock_list = []

    # Look up all current stock values
    current_stock_values = multiple_lookup(sorted_stock_list)

    # Iterate over sorted, unique stock symbols
    for unique_stock in sorted_stock_list:
        # Set "unique_stock_shares" variable to 0 for each unique stock
        unique_stock_shares = 0
        # Iterate over stocks portfolio of current user
        stock_name = ''
        for stock in stock_portfolio:
            # Gives number of shares for each stock by adding each repeated
            # stock shares value to current unique stock

            if stock.symbol == unique_stock:
                unique_stock_shares += int(stock.shares)
                stock_name = stock.name

        # Get current unique stock value (via lookup)
        stock_price = float(current_stock_values[unique_stock])
        # Get total price of all shares for unique stock
        stock_total = stock_price * unique_stock_shares
        # Only update stock_list if user owns stocks
        if stock_total > 0:
            # Append dictionary to stock list with all known info about stock
            stock_list.append(
                {"symbol": unique_stock,
                 "name": stock_name,
                 "shares": unique_stock_shares,
                 "price": stock_price,
                 "total": stock_total
                 })

    return stock_list


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
                extra_tags='stock'
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
                    extra_tags='stock'
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
            f'Given non-integer integer share count!',
            extra_tags='stock'
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

