from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Stock_change(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name}"

class Stock_info(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    current_price = models.IntegerField()
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name}"

class Stock_holding(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeginKey(Stock_info, on_delete=models.CASCADE)
    amount = models.IntegerField()
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name}"