from django.urls import path
from . import views

app_name = 'Finance'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('history/', views.History.as_view(), name='history'),
    path('add_funds/', views.AddFunds.as_view(), name='add_funds'),
    path('ajax_graph/', views.ajax_graph, name='ajax_graph'),
    path('ajax_quote/', views.ajax_quote, name='ajax_quote'),
    path('ajax_stock_list', views.ajax_stock_list, name='ajax_stock_list')
]
