from django.urls import path
from . import views

app_name = 'Finance'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('quote/', views.quote, name='quote'),
    path('history/', views.History.as_view(), name='history'),
    path('analysis/', views.analysis, name='analysis'),
    path('add_funds/', views.AddFunds.as_view(), name='add_funds'),
    path('ajax-graph/', views.ajax_graph, name='ajax_graph'),
    path('ajax_price/', views.ajax_price, name='ajax_price'),
]
