from django.urls import path
from games import views

app_name = 'games'

urlpatterns = [
    path('', views.home, name='index'),
    # path('twisted_towers/', , name='twisted_towers'),
]