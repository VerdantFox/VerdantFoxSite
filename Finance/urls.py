from django.urls import path
from . import views

app_name = 'Finance'

urlpatterns = [
    path('', views.portfolio, name='index'),
]
