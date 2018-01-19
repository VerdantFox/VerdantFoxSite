from django.shortcuts import render
from django.http import HttpResponse
from .models import Video


def home(request):
    return render(request, 'games/games_index.html')


def twisted_towers(request):

    ttvideo = Video.objects.get(name__exact='twisted_towers')
    # response = HttpResponse(s.getvalue())

    return render(request, 'games/twisted_towers.html',
                  {'ttvideo': ttvideo}
                  )
