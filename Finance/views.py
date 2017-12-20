from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'Finance/Finance_index.html')

