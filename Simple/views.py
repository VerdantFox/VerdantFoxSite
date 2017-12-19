from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import VigenereForm, FizzBuzzForm, ChangeForm
from .mini_apps.vigenere_cipher import vigenere_cipher
from .mini_apps.vigenere_decipher import vigenere_decipher
from .mini_apps.FizzBuzz import create_variables, fizz_buzz
from .mini_apps.Change import change_function
from django.views import generic


def home(request):
    return render(request, 'Simple/Simple_index.html')


def vigenere(request):
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
        vigenere_form = VigenereForm()

    return render(request, 'Simple/vigenere_form.html',
                  {'vigenere_form': vigenere_form})


def fizzbuzz(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        fizzbuzz_form = FizzBuzzForm(request.POST)
        # check whether it's valid:
        if fizzbuzz_form.is_valid():
            # process the data in form.cleaned_data as required
            count_to = fizzbuzz_form.cleaned_data['count_to']
            multiplier = fizzbuzz_form.cleaned_data['multiplier']
            var_1 = fizzbuzz_form.cleaned_data['var_1']
            var_2 = fizzbuzz_form.cleaned_data['var_2']
            var_3 = fizzbuzz_form.cleaned_data['var_3']
            var_1_multiple = fizzbuzz_form.cleaned_data['var_1_multiple']
            var_2_multiple = fizzbuzz_form.cleaned_data['var_2_multiple']
            var_3_multiple = fizzbuzz_form.cleaned_data['var_3_multiple']

            var_dict = create_variables(
                var_1, var_1_multiple, var_2, var_2_multiple,
                var_3, var_3_multiple)

            fizzbuzz_list = fizz_buzz(count_to, multiplier, var_dict)

            return render(request, 'Simple/fizzbuzz_form.html',
                          {'fizzbuzz_form': fizzbuzz_form,
                           'fizzbuzz_list': fizzbuzz_list})

    # if a GET (or any other method) we'll create a blank form
    else:
        fizzbuzz_form = FizzBuzzForm()

    return render(request, 'Simple/fizzbuzz_form.html',
                  {'fizzbuzz_form': fizzbuzz_form})


def change_machine(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        change_form = ChangeForm(request.POST)
        # check whether it's valid:
        if change_form.is_valid():
            # process the data in form.cleaned_data as required
            item_cost = change_form.cleaned_data['item_cost']
            amount_paid = change_form.cleaned_data['amount_paid']

            bills_statement, coins_statement, change = change_function(item_cost, amount_paid)

            return render(request, 'Simple/change_form.html',
                          {'change_form': change_form,
                           'bills_statement': bills_statement,
                           'coins_statement': coins_statement,
                           'change': change})

    # if a GET (or any other method) we'll create a blank form
    else:
        change_form = ChangeForm()

    return render(request, 'Simple/change_form.html',
                  {'change_form': change_form})
