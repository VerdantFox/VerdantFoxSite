from django.contrib import admin
from .models import Transaction, StockSymbolName, UserInfo

admin.site.register(Transaction)
admin.site.register(StockSymbolName)
admin.site.register(UserInfo)
