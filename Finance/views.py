from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .helpers import stock_index, single_lookup, get_stock_name
from django.views.generic import TemplateView, ListView
from .forms import QuoteForm, BuyForm
from .models import Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    # Iterate over stock_list adding together all stock "total" values

    user_cash = request.user.userinfo.cash

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
        user_timezone = self.request.user.userprofile.timezone
        timezone.activate(user_timezone)
        return transactions


def add_funds(request):
    """Add cash to account"""
    return render(request, 'Finance/add_funds.html')

    # if user reached route via POST (as by submitting a form via POST)
    # if request.method == "POST":
    #     # Ensure name is present and alpha
    #     name_temp = request.form.get("name")
    #     name_temp = name_temp.replace(" ", "")
    #     if not request.form.get("name"):
    #         return apology("Enter name")
    #     if name_temp.isalpha() == False:
    #         return apology("Cannot include symbols or numbers in name")
    #
    #     # Ensure credit card present
    #     if not request.form.get("card_number"):
    #         return apology("Enter credit card number!")
    #
    #     # Enusre card is valid
    #     if credit(request.form.get("card_number")) == False:
    #         return apology("invalid credit card number!")
    #
    #     # Ensure date is valid
    #     # https://stackoverflow.com/questions/32483997/get-current-date-time-and-compare-with-other-date
    #     current_date_time = datetime.datetime.now()
    #     card_date = request.form.get("month") + "/" + request.form.get("year")
    #     card_date = ExpectedDate = datetime.datetime.strptime(card_date, "%m/%Y")
    #     if current_date_time >= card_date:
    #         return apology("invalid expiration date")
    #
    #     # convert cash added to float without commas and 2 decimal places
    #     cash_added = str(request.form.get("cash"))
    #     try:
    #         # Ensure valid cash type and convert to float with 2 decimal places
    #         cash_added = float(cash_added)
    #         # https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
    #         cash_added = float("{0:.2f}".format(cash_added))
    #     except:
    #         return apology("invalid cash amount!")
    #     # Ensure cash within valid range
    #     if cash_added > 500000.00 or cash_added <= 0:
    #         return apology("invalid cash amount")
    #
    #     else:
    #         # history_symbol = "Cash added"
    #         # Update portfolio with cash additin
    #         history_update = db.execute("INSERT INTO portfolio (user_id, stock, number_of_shares, price)"
    #             " VALUES(:user_id, :stock, NULL, :price)", user_id=session["user_id"],
    #             stock="Cash added", price=cash_added)
    #         # Error if could not update portfolio
    #         if not history_update:
    #             return apology("Error: failed to create cash update in history")
    #         #update user's cash
    #         user_cash_update = db.execute("UPDATE users SET cash = cash + :cash_added WHERE id = :id", cash_added=cash_added, id=session["user_id"])
    #         if not user_cash_update:
    #             return apology("Error: failed to add cash")
    #         # Flash sold message
    #         flash("Cash added!")
    #         # redirect user to home page
    #         return redirect(url_for("index"))
    #
    # # else if user reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("add_cash.html")