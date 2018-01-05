from django.contrib import admin
from .models import StockPurchase, StockSymbolName, UserCash

admin.site.register(StockPurchase)
admin.site.register(StockSymbolName)
admin.site.register(UserCash)
