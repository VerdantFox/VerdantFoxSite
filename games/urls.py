from django.urls import path
from games import views

app_name = 'games'

urlpatterns = [
    path('', views.home, name='index'),
    path('twisted_towers/', views.twisted_towers, name='twisted_towers'),
    path('battys_moth_hunt/', views.moth_hunt, name='moth_hunt'),
    path('connect_4/', views.connect_4, name='connect_4'),
]
