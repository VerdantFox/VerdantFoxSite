from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings


app_name = 'accounts'

urlpatterns = [
    path('', views.view_profile),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),

    # https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
    # https://docs.djangoproject.com/en/2.0/topics/auth/default/
    path('password_reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/reset/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
