import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VerdantFox.settings')

import django
django.setup()

import csv

from Finance.models import StockInfo

with open('COMBO_names.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = StockInfo(
            symbol=row['symbol'], name=row['name'])
        p.save()

print("Stocks updated!")
