from django.urls import path

from . import views
from .views import index_views, stock_list_views, stock_page_views

app_name = 'myapp'

urlpatterns = [
    path("", index_views.index, name="index"),
    path("stock-list", stock_list_views.stock_list, name="stock-list"),
    path("stock-page/<code>", stock_page_views.stock_page, name="stock-page"),
    path('stock-page/<code>/create/', stock_page_views.post_create, name= 'post_create'),
]