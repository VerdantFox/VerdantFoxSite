from django.urls import path
from . import views

app_name = 'Finance'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
]
