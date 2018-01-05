from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class StockPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=12)
    name = models.CharField(max_length=50)
    shares = models.PositiveIntegerField()
    price = models.FloatField()
    time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f"{self.symbol}: {self.shares} shares"


class StockSymbolName(models.Model):
    stock_symbol = models.CharField(max_length=12)
    stock_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('stock_symbol',)

    def __str__(self):
        return f"{self.stock_symbol} is {self.stock_name} shares"


class UserCash(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.FloatField()

    def __str__(self):
        return f"${self.cash:,.2f}"


@receiver(post_save, sender=User)
def create_user_cash(sender, instance, created, **kwargs):
    if created:
        UserCash.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_cash(sender, instance, **kwargs):
    instance.usercash.save()
