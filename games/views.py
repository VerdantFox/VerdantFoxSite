from django.shortcuts import render


def home(request):
    return render(request, 'games/games_index.html')