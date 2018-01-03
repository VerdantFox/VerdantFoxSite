from django.db import models
from django.contrib.auth.models import User


class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=12)
    name = models.CharField(max_length=30)
    shares = models.IntegerField()
    price = models.FloatField()
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol}: {self.shares} shares"
