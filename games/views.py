from django.shortcuts import render


def home(request):
    return render(request, 'games/games_index.html')


def twisted_towers(request):
    return render(request, 'games/twisted_towers.html')
