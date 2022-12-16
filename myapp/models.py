from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    stock_amount = models.IntegerField()
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name}"