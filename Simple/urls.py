from django.urls import path
from Simple import views

app_name = 'Simple'

urlpatterns = [
    path('', views.home, name='home'),
    path('vigenere/', views.vigenere, name='vigenere'),
    path('fizzbuzz/', views.fizzbuzz, name='fizzbuzz'),
    path('change/', views.change_machine, name='change_machine'),
]
