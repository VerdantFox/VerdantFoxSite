from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import VigenereForm
from .mini_apps.vigenere_cipher import vigenere_cipher
from .mini_apps.vigenere_decipher import vigenere_decipher
from django.views import generic


def home(request):
    return render(request, 'Simple/Simple_index.html')


def vigenere(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        vigenere_form = VigenereForm(request.POST)
        # check whether it's valid:
        if vigenere_form.is_valid():

            # process the data in form.cleaned_data as required
            cipher_key = vigenere_form.cleaned_data['cipher_key']
            input_text = vigenere_form.cleaned_data['input_text']
            # Encrypt with vigenere cipher
            if "encrypt" in request.POST:
                encrypted_text = vigenere_cipher(cipher_key, input_text)
                # Rather than redirect, return to same page with new information
                # (cipher_key and encrypted_text)
                return render(request, 'Simple/vigenere_form.html',
                              {'vigenere_form': vigenere_form,
                               'cipher_key': cipher_key,
                               'encrypted_text': encrypted_text})
            # Decrypt with vigenere cipher
            elif "decrypt" in request.POST:
                decrypted_text = vigenere_decipher(cipher_key, input_text)
                # Rather than redirect, return to same page with new information
                # (cipher_key and decrypted_text)
                return render(request, 'Simple/vigenere_form.html',
                              {'vigenere_form': vigenere_form,
                               'cipher_key': cipher_key,
                               'decrypted_text': decrypted_text})

    # if a GET (or any other method) we'll create a blank form
    else:
        if pk:
            print(pk)
            print(type(pk))
        vigenere_form = VigenereForm()

    return render(request, 'Simple/vigenere_form.html',
                  {'vigenere_form': vigenere_form})
