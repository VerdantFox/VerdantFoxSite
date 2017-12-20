from django.shortcuts import render
# from django.contrib.auth import
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms


class SignUp(CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'


