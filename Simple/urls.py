from django.urls import path
from Simple import views

app_name = 'Simple'

urlpatterns = [
    path('', views.home, name='index'),
    # path('vigenere/', views.VigenereView.as_view(), name='vigenere'),
    path('vigenere/', views.vigenere, name='vigenere'),
    # path('vigenere/<int:pk>/results/', views.vigenere_results,
    #      name='vigenere_results')
    path('vigenere/<int:pk>/encrypt/results/',
         views.EncryptionResultsView.as_view(),
         name='vigenere_encrypt_results'),
    path('vigenere/<int:pk>/decrypt/results/',
         views.DecryptionResultsView.as_view(),
         name='vigenere_decrypt_results'),

    # path('vigenere/empty/results/', views.EncryptionResultsView.as_view(),
    #      name='vigenere_results'),
    # path('vigenere/results/', views.EncryptionResultsView.as_view(),
    #      name='vigenere_results'),
]
