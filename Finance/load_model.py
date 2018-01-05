import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VerdantFox.settings')

import django
django.setup()

import csv

from Finance.models import StockSymbolName

with open('COMBO_names.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = StockSymbolName(
            stock_symbol=row['stock_symbol'], stock_name=row['stock_name'])
        p.save()
