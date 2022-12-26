from django.urls import path

from . import views
from .views import index_views, stock_list_views

app_name = 'myapp'

urlpatterns = [
    path("", index_views.index, name="index"),
    path("stock-list", stock_list_views.stock_list, name="stock-list"),
]