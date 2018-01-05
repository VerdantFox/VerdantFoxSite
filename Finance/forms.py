from django import forms
from .models import StockPurchase


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
            print('form clean symbol')
            symbol = self.cleaned_data['symbol']

            if not symbol.isalpha():
                raise forms.ValidationError(
                    "Stock symbol must be alphabetical")


class BuyForm(forms.ModelForm):
    class Meta:
        model = StockPurchase
        fields = ('symbol', 'shares',)

    symbol = forms.CharField(
        label="Stock symbol:",
        max_length=5,
        widget=forms.HiddenInput())

    shares = forms.IntegerField(
        label='Purchase shares:',
        widget=forms.NumberInput(attrs={
            'name': 'shares',
            'placeholder': 'number of shares',
            'class': 'form-control',
        }))
    price = forms.FloatField(
        label='stock price:',
        widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        if 'shares' in self.cleaned_data:
            print('form clean shares')
            shares = self.cleaned_data['shares']

            if shares <= 0:
                raise forms.ValidationError(
                    "Must purchase a positive number of shares.")

