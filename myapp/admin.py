from django.contrib import admin

from .models import Stock_change, Stock_holding, Stock_info

# Register your models here.
admin.site.register(Stock_change)
admin.site.register(Stock_holding)
admin.site.register(Stock_info)