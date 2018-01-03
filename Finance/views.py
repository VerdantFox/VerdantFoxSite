from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .helpers import stock_index


@login_required
def portfolio(request):
    """ List users stock portfolio, cash and net worth """
    stock_list = stock_index(request.user)

    # Create a variable for finding the combined worth of all owned stocks
    total_stock_worth = 0
    # Iterate over stock_list adding together all stock "total" values

    # TODO make user_cash
    # user_cash temporarily $5000
    user_cash = 5000.00

    for totals in stock_list:
        totals_float = totals["total"].replace("$", "")
        totals_float = totals_float.replace(",", "")
        total_stock_worth += float(totals_float)

    # Find net worth (cash + total stock value)
    net_worth = user_cash + total_stock_worth

    user_cash = f"${user_cash:,.2f}"
    net_worth = f"${net_worth:,.2f}"
    return render(request, 'Finance/Finance_index.html', context={
        "stock_list": stock_list,
        "cash": user_cash,
        "net_worth": net_worth
    })



