from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import VigenereForm


def home(request):
    return render(request, 'Simple/Simple_index.html')


def vigenere(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VigenereForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            cipher_key = data['cipher_key']
            plain_text = data['plain_text']
            print(cipher_key, plain_text)

            # redirect to a new URL:
            return HttpResponseRedirect(
                reverse('Simple:vigenere_results'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VigenereForm()

    return render(request, 'Simple/vigenere_form.html', {'form': form})


def results(request):
    return render(request, 'Simple/vigenere_results.html')
