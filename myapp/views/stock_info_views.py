from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Stock_change, Stock_holding, Stock_info

def stock_info(request, code):
    stock_info = Stock_info.objects.get(code=code)
    stock_name = stock_info.name
    return render(request, "myapp/stock_info.html", {
        "stock_name": stock_name
    })