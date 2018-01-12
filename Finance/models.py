from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=12)
    name = models.CharField(max_length=50)
    shares = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f"{self.symbol}: {self.shares} shares"


class StockInfo(models.Model):
    # Cache name and symbol in database (from CSV file)
    # http://www.nasdaq.com/screening/company-list.aspx
    symbol = models.CharField(max_length=12)
    name = models.CharField(max_length=50)

    # Cache most recent stock price in database (and datetime of update)
    price = models.FloatField(null=True, blank=True)
    price_update_time = models.DateTimeField(null=True, blank=True)

    # Cache json data for stock graphs (and datetime of updates)
    day_json = JSONField(null=True, blank=True)
    day_json_update_time = models.DateTimeField(null=True, blank=True)

    # Cache json data for stock graphs (and datetime of updates)
    week_json = JSONField(null=True, blank=True)
    week_json_update_time = models.DateTimeField(null=True, blank=True)

    # Cache json data for stock graphs (and datetime of updates)
    month_json = JSONField(null=True, blank=True)
    month_json_update_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('symbol',)

    def __str__(self):
        return f"{self.symbol}, {self.name}"


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.FloatField(default=10000)

    def __str__(self):
        return f"{self.user.username}: ${self.cash:,.2f}"


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()
