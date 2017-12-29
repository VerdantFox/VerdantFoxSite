from django.contrib import admin
from .models import UserProfile, Activation


admin.site.register(UserProfile)
admin.site.register(Activation)
