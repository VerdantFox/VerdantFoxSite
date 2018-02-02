from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/',
    #      views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
    #      name='logout'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),
]
