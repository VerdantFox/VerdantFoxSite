from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


class Activation(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                             primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20)
    email = models.EmailField(blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics',
        blank=True)
    bio = models.CharField(max_length=500, default='')
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
