from django.shortcuts import render
from . import forms


def vigenere_view(request):
    form = forms.VigenereForm()
    return render(request, 'templates/vigenere_form.html', {'form': form})
