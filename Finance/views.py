from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .helpers import stock_index, single_lookup, get_stock_name
from django.views.generic import TemplateView
from .forms import QuoteForm, BuyForm
from .models import StockPurchase
from django.http import HttpResponseRedirect
from django.urls import reverse


class Home(TemplateView):
    """Display static page with information about app"""
    template_name = 'Finance/Finance_index.html'


@login_required()
def portfolio(request):
    """List users stock portfolio, cash and net worth"""
    stock_list = stock_index(request.user)

    # Create a variable for finding the combined worth of all owned stocks
    total_stock_worth = 0
    # Iterate over stock_list adding together all stock "total" values

    # TODO make user_cash
    # user_cash temporarily $5000
    user_cash = request.user.usercash.cash

    for totals in stock_list:
        totals_float = totals["total"].replace("$", "")
        totals_float = totals_float.replace(",", "")
        total_stock_worth += float(totals_float)

    # Find net worth (cash + total stock value)
    net_worth = user_cash + total_stock_worth

    user_cash = f"${user_cash:,.2f}"
    net_worth = f"${net_worth:,.2f}"

    return render(request, 'Finance/portfolio.html', context={
        "stock_list": stock_list,
        "cash": user_cash,
        "net_worth": net_worth
    })


@login_required()
def quote(request):
    """Get stock quote. Allow purchase of quoted stock."""
    error = None
    buy_form = None
    symbol = None
    name = None
    price = None
    quote_form = None
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if "get quote" in request.POST:
            print("here")
            # create a form instance and populate it with data from quote
            quote_form = QuoteForm(request.POST)
            # Check if valid
            if quote_form.is_valid():
                # process the data in form.cleaned_data as required
                symbol = quote_form.cleaned_data['symbol'].upper()
                print(symbol)
                try:
                    name = get_stock_name(symbol)
                except:
                    name = None
                print(name)
                if name:
                    price = single_lookup(symbol)
                else:
                    price = "Error, could not find stock."
                print(price)

                quote_form = QuoteForm()
                if isinstance(price, str):
                    error = price
                    price = None
                else:
                    buy_form = BuyForm(initial={'symbol': symbol,
                                                'price': price})
                    price = f'${price:,.2f}'

        if "buy" in request.POST:
            # create a form instance and populate it with data from quote
            buy_form = BuyForm(request.POST)
            quote_form = QuoteForm()
            if buy_form.is_valid():
                # process the data in form.cleaned_data as required
                symbol = buy_form.cleaned_data['symbol'].upper()
                print(f'stock symbol: {symbol}')
                try:
                    name = get_stock_name(symbol)
                except:
                    name = None
                print(f'stock name: {name}')
                shares = buy_form.cleaned_data['shares']
                total_cost = None
                print(f'shares: {shares}')
                if name:
                    # price = single_lookup(symbol)
                    price = buy_form.cleaned_data['price']
                    print(f"this is still the price: {price}")
                    total_cost = price * shares
                else:
                    price = None
                print(f'stock price: {price}')

                user_cash = request.user.usercash

                if name and shares and user_cash and total_cost:
                    if user_cash.cash >= total_cost:
                        purchase = StockPurchase(user=request.user,
                                                 symbol=symbol,
                                                 name=name,
                                                 shares=shares,
                                                 price=price)
                        original_cash = user_cash.cash
                        user_cash.cash -= total_cost
                        if purchase and original_cash != user_cash:
                            user_cash.save()
                            purchase.save()
                            return HttpResponseRedirect(
                                reverse('Finance:portfolio'))
                        else:
                            error = "Could not save file"
                    else:
                        error = "Not enough funds to make that purchase."

    else:
        quote_form = QuoteForm()

    return render(request, 'Finance/quote.html',
                  {'quote_form': quote_form,
                   'buy_form': buy_form,
                   'price': price,
                   'symbol': symbol,
                   'name': name,
                   'error': error})
