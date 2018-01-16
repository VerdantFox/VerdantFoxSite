from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .helpers import (stock_index, single_lookup, search_stock_info,
                      check_repeats, validate_shares)
from django.views.generic import TemplateView, ListView, FormView, base
from .forms import QuoteForm, BuyForm, AddFundsForm, AnalysisForm
from .models import Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone
# from django.core.paginator import Pa
from .bgraph import bokeh_graph

# tests
from .models import StockInfo
import datetime


class Home(TemplateView):
    """Display static page with information about app"""
    template_name = 'Finance/Finance_index.html'


@login_required()
def ajax_stock_list(request):
    # These value's are none unless otherwise specified
    error = None
    buy_form = None

    # Get user's stock list
    stock_list = stock_index(request.user)
    # if failed return empty portfolio with error
    if isinstance(stock_list, str):
        return render(request, 'Finance/ajax_stock_list.html', context={
            'error': stock_list
        })

    # Create a variable for finding the combined worth of all owned stocks
    total_stock_worth = 0

    # get users funds
    user_funds = request.user.userinfo.cash

    # Iterate over stock_list adding together all stock "total" values
    for stock in stock_list:
        total_stock_worth += stock['total']

    # Find net worth (cash + total stock value)
    net_worth = user_funds + total_stock_worth

    user_funds = f"${user_funds:,.2f}"
    net_worth = f"${net_worth:,.2f}"

    if request.method == "POST":

        # Did request come from the quote "buy" form
        if "buy" in request.POST:
            print("BUY WAS IN REQUEST.POST")
            # create a form instance and populate it with data from quote
            buy_form = BuyForm(request.POST)
            if buy_form.is_valid():
                # process the data in form.cleaned_data as required
                symbol = buy_form.cleaned_data['symbol'].upper()
                shares = buy_form.cleaned_data['buy_shares']
                # Get name and price from symbol
                name, price = search_stock_info(symbol)
                # multiply for total transaction cost
                total_cost = price * shares
                # get user info
                user_info = request.user.userinfo
                # Check essential transaction attributes present
                if name and shares and user_info and total_cost:
                    # Check user can afford purchase
                    if user_info.cash >= total_cost:
                        # set up transaction
                        purchase = Transaction(user=request.user,
                                               symbol=symbol,
                                               name=name,
                                               shares=shares,
                                               price=price,
                                               total=total_cost
                                               )
                        # Remember user's old cash and define new cash
                        original_cash = user_info.cash
                        user_info.cash -= total_cost
                        # Only save if model went through and user cash updated
                        if purchase and original_cash != user_info:
                            # Save both models
                            user_info.save()
                            purchase.save()
                            # Define plurality of 'share' for success statement
                            if shares == 1:
                                share_plural = 'share'
                            else:
                                share_plural = 'shares'
                            # Success statement
                            messages.add_message(
                                request, messages.SUCCESS,
                                f'Bought {shares} {share_plural} '
                                f'of {name} ({symbol})!',
                                extra_tags='stock buy-success'
                            )
                        # transaction was entered correctly
                        # or user cash not changed
                        else:
                            error = "Could not save file"
                    # total cost greater than user's funds
                    else:
                        error = "Not enough funds to make that purchase."
                        price = f'${price:,.2f}'

            # Update user's stock list
            stock_list = stock_index(request.user)
            # if failed return empty portfolio with error
            if isinstance(stock_list, str):
                return render(request, 'Finance/ajax_stock_list.html',
                              context={
                                  'error': stock_list
                              })

        # Request didn't come from "buy"
        else:
            user_info = request.user.userinfo
            # Create dictionary of user's stocks.
            # stock_dict['symbol'] = (name, shares owned, stock price)
            stock_dict = {}
            for stock in stock_list:
                stock_dict[stock['symbol']] = stock['name'], stock['shares'], stock['price'],

            repeat_list = check_repeats(request.POST)
            transaction_made = False
            for item in request.POST:
                stock_symbol = None
                if item[:3] == "buy" or item[:4] == "sell":
                    # Split item to get buy/sell:0 and stock symbol:1
                    split_item = item.split('-')
                    # Get stock symbol
                    stock_symbol = split_item[1].upper()

                    if stock_symbol in repeat_list and item[:4] == "sell":
                        messages.add_message(
                            request, messages.WARNING,
                            f'Could not resolve {stock_symbol}. Listed as '
                            f'both "buy" and "sell"!',
                            extra_tags='stock'
                        )

                # Check if item name starts with "buy" and isn't repeat
                if stock_symbol not in repeat_list and item[:3] == "buy":

                    # Check if item was bought bought
                    if request.POST[item]:
                        # List there was a transaction (for error)
                        transaction_made = True
                        # Check if share count is valid and get integer back
                        valid_shares = validate_shares(request, stock_symbol, request.POST[item])
                        if valid_shares:
                            # Get stock shares and price
                            name, owned_shares, price = stock_dict[stock_symbol]
                            price = float(price)
                            # Get total cost of transaction
                            purchase_cost = valid_shares * price

                            # If user can afford purchase, buy stocks
                            if purchase_cost <= user_info.cash:

                                try:
                                    # Subtract purchase cost from user account
                                    user_info.cash -= purchase_cost
                                    # Record transaction
                                    purchase = Transaction(user=request.user,
                                                           symbol=stock_symbol,
                                                           name=name,
                                                           shares=valid_shares,
                                                           price=price,
                                                           total=purchase_cost
                                                           )
                                    # Save models
                                    user_info.save()
                                    purchase.save()
                                    # Check plural for success message
                                    if valid_shares == 1:
                                        share_plural = 'share'
                                    else:
                                        share_plural = 'shares'
                                    # Success message
                                    messages.add_message(
                                        request, messages.SUCCESS,
                                        f'Bought {valid_shares} {share_plural} '
                                        f'of {name} ({stock_symbol})!',
                                        extra_tags='stock buy-success'
                                        )

                                except:
                                    messages.add_message(
                                        request, messages.WARNING,
                                        f'Failed {stock_symbol} purchase!',
                                        extra_tags='stock'
                                    )

                            else:
                                messages.add_message(
                                    request, messages.WARNING,
                                    f'Failed to purchase{stock_symbol}, '
                                    f'not enough funds!',
                                    extra_tags='stock'
                                )

                # Check if item name starts with "sell"
                if stock_symbol not in repeat_list and item[:4] == "sell":

                    # Check if item was sold
                    if request.POST[item]:
                        # List there was a transaction (for error)
                        transaction_made = True
                        # Get stock shares and price
                        name, owned_shares, price = stock_dict[stock_symbol]
                        owned_shares = int(owned_shares)
                        price = float(price)

                        # Check if share count is valid and get integer back
                        valid_shares = validate_shares(
                            request, stock_symbol, request.POST[item], owned_shares)

                        if valid_shares:
                            # Get total cost of transaction
                            sale_value = valid_shares * price

                            try:
                                # Add add sale value to user account
                                user_info.cash += sale_value
                                # Record transaction
                                sale = Transaction(user=request.user,
                                                   symbol=stock_symbol.upper(),
                                                   name=name,
                                                   shares=-valid_shares,
                                                   price=price,
                                                   total=sale_value
                                                   )
                                # Save models
                                user_info.save()
                                sale.save()

                                # Check plural for success message
                                if valid_shares == 1:
                                    share_plural = 'share'
                                else:
                                    share_plural = 'shares'
                                # Success message
                                messages.add_message(
                                    request, messages.SUCCESS,
                                    f'Sold {valid_shares} {share_plural} '
                                    f'of {name} ({stock_symbol})!',
                                    extra_tags='stock sale-success'
                                )
                            except:
                                messages.add_message(
                                    request, messages.WARNING,
                                    f'Failed {stock_symbol} sale!',
                                    extra_tags='stock'
                                )

            if transaction_made:
                # Get user's stock list again (after transactions)
                stock_list = stock_index(request.user)
                # if failed return empty portfolio with error
                if isinstance(stock_list, str):
                    return render(request, 'Finance/ajax_stock_list.html',
                                  context={'error': stock_list})
            else:
                messages.add_message(
                    request, messages.WARNING,
                    f'No purchases or sales indicated.',
                    extra_tags='stock'
                )

    # request.method isn't POST (probably GET)
    else:
        # Do nothing
        pass

    # Format stock money values for template view
    for stock in stock_list:
        stock['price'] = f"${stock['price']:,.2f}"
        stock['total'] = f"${stock['total']:,.2f}"

    return render(request, 'Finance/ajax_stock_list.html', context={
        "error": error,
        "buy_form": buy_form,
        "stock_list": stock_list,
        "funds": user_funds,
        "net_worth": net_worth,
    })


@login_required()
def portfolio(request):
    """List users stock portfolio, cash and net worth"""
    # Load up form for getting new quotes
    quote_form = QuoteForm()

    # All other functionality for portfolio moved to within ajax_quote
    # and within ajax_stock_list views

    return render(request, 'Finance/portfolio.html', context={
        "quote_form": quote_form,
    })


@login_required()
def ajax_quote(request):
    quote_form = None
    buy_form = None
    price = None
    symbol = None
    name = None
    error = None

    if request.method == "POST":
        if "quote" in request.POST:
            # create a form instance and populate it with data from quote
            quote_form = QuoteForm(request.POST)
            # Check if valid
            if quote_form.is_valid():
                # process the data in form.cleaned_data as required
                symbol = quote_form.cleaned_data['symbol'].upper()

                # Get stock name and price
                name, price = search_stock_info(symbol)
                # Reset quote form for searching up new stock
                quote_form = QuoteForm()
                if name and price:
                    buy_form = BuyForm(initial={'symbol': symbol})
                    price = f'${price:,.2f}'
                else:
                    error = "Error, could not find stock"

    return render(request, 'Finance/ajax_quote.html',
                  {'quote_form': quote_form,
                   'buy_form': buy_form,
                   'price': price,
                   'symbol': symbol,
                   'name': name,
                   'error': error})


class History(LoginRequiredMixin, ListView):
    """Display users purchase, sale, and money addition history"""
    template_name = 'Finance/history.html'
    model = Transaction
    paginate_by = 10
    paginate_orphans = 9

    def get_queryset(self):
        transactions = self.model.objects.filter(
            user=self.request.user).order_by('-time_stamp')
        for transaction in transactions:
            if transaction.shares == 0:
                transaction.shares = ''
            if transaction.price == 0:
                transaction.price = ''
            else:
                transaction.price = f'${transaction.price:,.2f}'
            transaction.total = f'${transaction.total:,.2f}'

        user_timezone = self.request.user.userprofile.timezone
        timezone.activate(user_timezone)

        return transactions


@login_required()
def ajax_graph(request):
    # No graph script or div until valid one is returned
    script = None
    div = None
    # No symbol or time frame unless one is returned
    symbol = None
    time_frame = None
    # No error's until one arises
    graph_error = None

    if request.method == 'POST':
        for item in request.POST:
            if item[:6] == 'symbol':
                symbol, time_frame = item.split(',')
                symbol, time_frame = symbol.split(':'), time_frame.split(':')
                symbol, time_frame = symbol[1], time_frame[1].replace('-', ' ')

        script, div = bokeh_graph(symbol, time_frame)

        if not div:
            print('Got error making graph')
            graph_error = script
            script = None

    return render(request, 'Finance/ajax_graph.html',
                  {
                   'symbol': symbol,
                   'time_frame': time_frame,
                   'script': script,
                   'div': div,
                   'graph_error': graph_error
                   })


class AddFunds(LoginRequiredMixin, FormView, base.ContextMixin):
    template_name = 'Finance/add_funds.html'
    form_class = AddFundsForm
    success_url = reverse_lazy('Finance:portfolio')

    def get_context_data(self, **kwargs):
        cash = self.request.user.userinfo.cash
        context = super().get_context_data(**kwargs)
        context['cash'] = f'${cash:,.2f}'
        return context

    def form_valid(self, form):

        funds = form.cleaned_data.get('funds')
        name = form.cleaned_data.get('name')
        card_number = form.cleaned_data.get('card_number')
        cc_exp = form.cleaned_data.get('cc_exp')
        cvv = form.cleaned_data.get('cvv')
        zip_code = form.cleaned_data.get('zip_code')
        user_info = self.request.user.userinfo

        transaction = Transaction(
            user=self.request.user,
            symbol='FUNDS ADDED',
            name='',
            price=0,
            shares=0,
            total=funds
        )
        transaction.save()
        user_info.cash += funds
        user_info.save()
        messages.add_message(
            self.request, messages.SUCCESS,
            f'Added ${funds:,.2f} to your account!')

        return HttpResponseRedirect(reverse_lazy('Finance:portfolio'))
