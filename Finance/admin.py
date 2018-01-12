from django.contrib import admin
from .models import Transaction, StockInfo, UserInfo

admin.site.register(Transaction)
admin.site.register(StockInfo)
admin.site.register(UserInfo)
