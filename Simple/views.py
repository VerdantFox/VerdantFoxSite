from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import VigenereForm
from .mini_apps.vigenere_cipher import vigenere_cipher
from .mini_apps.vigenere_decipher import vigenere_decipher
from django.views.generic.edit import FormView
from .models import Encryption, Decryption
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
                print("encrypting")
                encrypted_text = vigenere_cipher(cipher_key, input_text)
                print(encrypted_text)

                # Create and instantiate instance of Encryption model
                encrypt_object = Encryption(
                    encryption_key=cipher_key,
                    plain_text=input_text,
                    encrypted_text=encrypted_text
                )
                encrypt_object.save()

                return HttpResponseRedirect(
                    reverse('Simple:vigenere_encrypt_results', args=(
                        encrypt_object.pk,)))

            elif "decrypt" in request.POST:

                print("decrypting")
                decrypted_text = vigenere_decipher(cipher_key, input_text)
                print(decrypted_text)

                # Create and instantiate instance of Decryption model
                decrypt_object = Decryption(
                    encryption_key=cipher_key,
                    encrypted_text=input_text,
                    decrypted_text=decrypted_text
                )
                decrypt_object.save()

                # redirect to a new URL (with pk arg):
                return HttpResponseRedirect(
                    reverse('Simple:vigenere_decrypt_results', args=(
                        decrypt_object.pk,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        vigenere_form = VigenereForm()

    return render(request, 'Simple/vigenere_form.html',
                  {'vigenere_form': vigenere_form})


class EncryptionResultsView(generic.DetailView):
    model = Encryption
    template_name = "Simple/vigenere_results.html"


class DecryptionResultsView(generic.DetailView):
    model = Decryption
    template_name = "Simple/vigenere_results.html"
