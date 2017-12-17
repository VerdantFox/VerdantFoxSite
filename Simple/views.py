from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import VigenereForm
from .mini_apps.vigenere_cipher import vigenere_cipher
from django.views.generic.edit import FormView
from .models import Encryption, Decryption
from django.views import generic


def home(request):
    return render(request, 'Simple/Simple_index.html')


def vigenere(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        encrypt_form = VigenereForm(request.POST)
        # check whether it's valid:
        if encrypt_form.is_valid():
            # process the data in form.cleaned_data as required
            cipher_key = encrypt_form.cleaned_data['cipher_key']
            plain_text = encrypt_form.cleaned_data['plain_text']
            # Encrypt with vigenere cipher
            encrypted_text = vigenere_cipher(cipher_key, plain_text)
            # Create and instantiate instance of Encryption model
            encrypt_object = Encryption(
                encryption_key=cipher_key,
                plain_text=plain_text,
                encrypted_text=encrypted_text
            )
            encrypt_object.save()
            # redirect to a new URL (with pk arg):
            return HttpResponseRedirect(
                reverse('Simple:vigenere_results', args=(
                    encrypt_object.pk,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        encrypt_form = VigenereForm()

    return render(request, 'Simple/vigenere_form.html',
                  {'encrypt_form': encrypt_form})


class EncryptionResultsView(generic.DetailView):
    model = Encryption
    template_name = "Simple/vigenere_results.html"
