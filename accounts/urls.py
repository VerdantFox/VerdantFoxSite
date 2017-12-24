from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    path('registered/', views.SignUpSuccess.as_view(), name='registered'),
]
