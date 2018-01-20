from django.shortcuts import render
from django.http import HttpResponse
from .models import Video


def home(request):
    return render(request, 'games/games_index.html')


def twisted_towers(request):
    # ttvideo = Video.objects.get(name__exact='twisted_towers')

    return render(request, 'games/twisted_towers.html')


def moth_hunt(request):
    return render(request, 'games/moth_hunt.html')
