import urllib.request
import json
import math
from .models import UserStock


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
            print(f"error with '{symbol}' symbol")
        if not 0 < len(symbol) < 6:
            print(f"error with '{symbol}' symbol")
        # Add symbol to the set
        query += symbol.upper() + ','

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:
        # GET JSON webpage
        webpage = f"https://www.alphavantage.co/query?function=BATCH_STOCK_" \
                  f"QUOTES&symbols={query}&apikey=1PSE4E7QME3PUPTU"

        # Convert JSON data from webpage into readable format
        # https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        with urllib.request.urlopen(webpage) as url:
            data = json.loads(url.read().decode())
            # Get the stock symbol and it's associated price
            for stock_info in data['Stock Quotes']:
                stock_symbol = stock_info['1. symbol']
                stock_price = f"{float(stock_info['2. price']):.2f}"
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

        # GET JSON webpage
        webpage = f"https://www.alphavantage.co/query?function=BATCH_STOCK_" \
                  f"QUOTES&symbols={symbol}&apikey=1PSE4E7QME3PUPTU"

        # Convert JSON data from webpage into readable format
        # https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        with urllib.request.urlopen(webpage) as url:
            data = json.loads(url.read().decode())
            # Get the stock symbol and it's associated price
            if data['Stock Quotes'] == {}:
                return "Error, stock not found."
            else:
                for stock_info in data['Stock Quotes']:
                    stock_symbol = stock_info['1. symbol']
                    stock_price = f"{float(stock_info['2. price']):.2f}"
                    return stock_symbol, stock_price

    except:
        return "Error getting or reading web page."


def stock_index(user):
    """Given a user, return list of stocks"""

    # Query database for unique stock symbols in "portfolio" from current user
    unique_stocks = UserStock.objects.values('symbol').distinct().filter(user__exact=user)

    # Query database for all info in "portfolio" from current user
    stock_portfolio = UserStock.objects.filter(user__exact=user)

    # Make a list to sort unique stocks
    presorted_stock_list = []
    # Iterate over unique stocks, converting each dict to a single string
    for stock in unique_stocks:
        presorted_stock_list.append(stock["symbol"])
    # If "Cash added" is in our list, remove it from our list
    if "Cash added" in presorted_stock_list:
        presorted_stock_list.remove("Cash added")
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
                 "price": f"${stock_price:,.2f}",
                 "total": f"${stock_total:,.2f}"
                 })

    return stock_list


def credit(card_number):
    """ Given a credit card, return True for valid or False for invalid """

    # Convert card number to string.
    card_number = str(card_number)
    # Remove empty space and dashes
    card_number = card_number.replace("-", "")
    card_number = card_number.replace(" ", "")

    # Number of digits in credit card number.
    c_length = len(card_number)
    # variable for our digit position on card string
    # (beginning with last digit in array)
    c_place = c_length - 1
    # initializing our checking formula to zero
    check_sum = 0

    """
    Valid cards require the following:
    1. Multiply every other digit by 2, starting with the number’s
        second-to-last digit, and then add those products' digits together.
    2. Add the sum to the sum of the digits that weren’t multiplied by 2.
    3. If the total’s last digit is 0, the number is valid!
    Accomplish these goals with a forever while loop
    that looks at each digit from end to front
    """
    try:
        while True:
            # If is the second to last digit or every other digit thereafter
            # (end to front) perform (1.) calculation from above^ notes
            # adding result to our check_sum
            if(c_length - c_place) % 2 == 0:
                tempa = (int(card_number[c_place]) * 2)
                check_sum += (math.floor((tempa % 100) / 10) +
                              math.floor(tempa % 10))
            # If the last digit or every other digit thereafter (end to front)
            # perform (2.) calculation from above^ notes adding result
            # to our check_sum
            elif(c_length - c_place) % 2 == 1:
                tempa = (int(card_number[c_place]))
                check_sum += math.floor(tempa % 10)
            # Travel backwards from last digit to first along credit card number
            c_place -= 1
            # Break loop after finishing with the first digit
            # in credit card number
            if c_place < 0:
                break
    except:
        return False

    # AMEX requirements = (3.) from above notes, 15 digits, starts with 34 or 37
    if((check_sum % 10 == 0) and (c_length == 15) and (int(card_number[0]) == 3)
            and ((int(card_number[1]) == 4) or (int(card_number[1]) == 7))):
        return True
    # MASTERCARD requirements = (3.) from above notes,
    # 16 digits, starts with 51, 52, 53, 54, or 55
    elif((check_sum % 10 == 0) and (c_length == 16)
         and (int(card_number[0]) == 5) and ((int(card_number[1]) > 0)
         and (int(card_number[1]) < 6))):
        return True
    # VISA requirements = (3.) from above notes, 13 or 16 digits, starts with 4
    elif((check_sum % 10 == 0) and (c_length == 13 or c_length == 16)
            and (int(card_number[0]) == 4)):
        return True
    # If none of above conditions met card is invalid.
    else:
        return False


if __name__ == "__main__":
    pass
