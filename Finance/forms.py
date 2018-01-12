from django import forms
from .models import Transaction, UserInfo
from .custom_formfields import CreditCardField
import datetime


class QuoteForm(forms.Form):
    symbol = forms.CharField(
        label="Look up stock by symbol:",
        max_length=5,
        widget=forms.TextInput(attrs={
            'name': 'stock symbol',
            'placeholder': 'Stock symbol',
            'class': 'form-control',
        }))

    def clean(self):
        super().clean()
        if 'symbol' in self.cleaned_data:
            symbol = self.cleaned_data['symbol']

            if not symbol.isalpha():
                raise forms.ValidationError(
                    "Stock symbol must be alphabetical")


class BuyForm(forms.Form):

    symbol = forms.CharField(
        label="Stock symbol:",
        max_length=5,
        widget=forms.HiddenInput())

    buy_shares = forms.IntegerField(
        required=False,
        label='Purchase shares:',
        widget=forms.NumberInput(attrs={
            'name': 'shares',
            'class': 'form-control',
        }))

    def clean(self):
        super().clean()
        if 'shares' in self.cleaned_data:
            shares = self.cleaned_data['buy_shares']
            if shares <= 0:
                raise forms.ValidationError(
                    "Must purchase a positive number of shares.")


class SellForm(forms.Form):

    symbol = forms.CharField(
        label="Stock symbol:",
        max_length=5,
        widget=forms.HiddenInput())

    sell_shares = forms.IntegerField(
        required=False,
        label='Purchase shares:',
        widget=forms.NumberInput(attrs={
            'name': 'shares',
            'class': 'form-control',
        }))
    price = forms.FloatField(
        label='stock price:',
        widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        if 'shares' in self.cleaned_data:
            print('form clean shares')
            shares = self.cleaned_data['sell_shares']

            if shares <= 0:
                raise forms.ValidationError(
                    "Must sell a positive number of shares.")


class AddFundsForm(forms.Form):
    funds = forms.FloatField(
        label="Funds to add",
        min_value=0.01, max_value=1000000.00,
        help_text="$1,000,000 largest amount allowed per addition.",
        widget=forms.NumberInput(attrs={
            'placeholder': '$25,000',
            'class': 'form-control',
        }))
    name = forms.CharField(
        label="Name", max_length=100,
        help_text="As it appears on card",
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }))
    card_number = CreditCardField(
        placeholder=u'0000 0000 0000 0000',
        min_length=12, max_length=19)
    cc_exp = forms.DateField(
        input_formats=['%m/%y'],
        label="Expiration",
        widget=forms.DateInput(attrs={
            'placeholder': 'MM/YY',
            'class': 'form-control',
        }))
    cvv = forms.IntegerField(
        label="Security code",
        min_value=100, max_value=9999,
        widget=forms.NumberInput(attrs={
            'placeholder': '123',
            'class': 'form-control',
        }))
    zip_code = forms.CharField(
        label="Postal code",
        max_length=10,
        widget=forms.NumberInput(attrs={
            'placeholder': '55555',
            'class': 'form-control',
        }))

    def clean_expiration_date(self):

        today = datetime.date.today()
        exp_date = self.cleaned_data['expiration_date']
        if exp_date < today:
            raise forms.ValidationError("Invalid date!!!")

        return exp_date
