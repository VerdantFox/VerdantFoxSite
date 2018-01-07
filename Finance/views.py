from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .helpers import (stock_index, single_lookup, get_stock_name,
                      check_repeats, validate_shares)
from django.views.generic import TemplateView, ListView, FormView, base
from .forms import QuoteForm, BuyForm, SellForm, AddFundsForm
from .models import Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils import timezone


class Home(TemplateView):
    """Display static page with information about app"""
    template_name = 'Finance/Finance_index.html'


@login_required()
def portfolio(request):
    """List users stock portfolio, cash and net worth"""
    stock_list = stock_index(request.user)

    # Create a variable for finding the combined worth of all owned stocks
    total_stock_worth = 0

    user_funds = request.user.userinfo.cash

    # Iterate over stock_list adding together all stock "total" values
    for stock in stock_list:
        total_stock_worth += stock['total']

    # Find net worth (cash + total stock value)
    net_worth = user_funds + total_stock_worth

    user_funds = f"${user_funds:,.2f}"
    net_worth = f"${net_worth:,.2f}"

    if request.method == "POST":
        user_info = request.user.userinfo
        # Create dictionary of user's stocks.
        # stock_dict['symbol'] = (name, shares owned, stock price)
        stock_dict = {}
        for stock in stock_list:
            stock_dict[stock['symbol']] = stock['name'], stock['shares'], stock['price'],

        repeat_list = check_repeats(request.POST)

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
                        f'both "buy" and "sell"!')

            # Check if item name starts with "buy" and isn't repeat
            if stock_symbol not in repeat_list and item[:3] == "buy":
                # Check if item was bought bought
                if request.POST[item]:

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
                                # Add add sale value to user account
                                user_info.cash -= purchase_cost
                                # Record transaction
                                purchase = Transaction(user=request.user,
                                                       symbol=stock_symbol,
                                                       name=name,
                                                       shares=valid_shares,
                                                       price=price)
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
                                    f'of {name} ({stock_symbol})!')

                            except:
                                messages.add_message(
                                    request, messages.WARNING,
                                    f'Failed {stock_symbol} purchase!')
                                pass
                        else:
                            messages.add_message(
                                request, messages.WARNING,
                                f'Failed to purchase{stock_symbol}, '
                                f'not enough funds!')

            # Check if item name starts with "sell"
            if stock_symbol not in repeat_list and item[:4] == "sell":
                # Check if item was sold
                if request.POST[item]:

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
                                               price=price)
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
                                f'of {name} ({stock_symbol})!')
                            return HttpResponseRedirect(
                                reverse('Finance:portfolio'))
                        except:
                            messages.add_message(
                                request, messages.WARNING,
                                f'Failed {stock_symbol} sale!')
                            pass

        return HttpResponseRedirect(
            reverse('Finance:portfolio'))

    else:
        pass

    # Format stock money values for template view
    for stock in stock_list:
        stock['price'] = f"${stock['price']:,.2f}"
        stock['total'] = f"${stock['total']:,.2f}"

    return render(request, 'Finance/portfolio.html', context={
        "stock_list": stock_list,
        "funds": user_funds,
        "net_worth": net_worth,
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
        if "quote" in request.POST:
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
                shares = buy_form.cleaned_data['buy_shares']
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

                user_info = request.user.userinfo

                if name and shares and user_info and total_cost:
                    if user_info.cash >= total_cost:
                        purchase = Transaction(user=request.user,
                                               symbol=symbol,
                                               name=name,
                                               shares=shares,
                                               price=price)
                        original_cash = user_info.cash
                        user_info.cash -= total_cost
                        if purchase and original_cash != user_info:
                            user_info.save()
                            purchase.save()
                            if shares == 1:
                                share_plural = 'share'
                            else:
                                share_plural = 'shares'
                            messages.add_message(
                                request, messages.SUCCESS,
                                f'Bought {shares} {share_plural} '
                                f'of {name} ({symbol})!')
                            return HttpResponseRedirect(
                                reverse('Finance:portfolio'))
                        else:
                            error = "Could not save file"
                    else:
                        error = "Not enough funds to make that purchase."
                        price = f'${price:,.2f}'

    else:
        quote_form = QuoteForm()

    return render(request, 'Finance/quote.html',
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

    def get_queryset(self):
        transactions = self.model.objects.filter(
            user=self.request.user).order_by('-time_stamp')
        for transaction in transactions:
            transaction.price = f'${transaction.price:,.2f}'
            if transaction.shares == 0:
                transaction.shares = ''
        user_timezone = self.request.user.userprofile.timezone
        timezone.activate(user_timezone)

        return transactions


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
            price=funds,
            shares=0,
        )
        # try:
        transaction.save()
        user_info.cash += funds
        user_info.save()
        messages.add_message(
            self.request, messages.SUCCESS,
            f'Added ${funds:,.2f} to your account!')
        # except:
        #     print("Transaction failed!")

        return HttpResponseRedirect(reverse_lazy('Finance:portfolio'))
