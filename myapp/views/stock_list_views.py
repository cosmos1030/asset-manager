from django.shortcuts import render, get_object_or_404
from json import dumps

from ..models import Stock_holding

def stock_list(request):
    stock_holding = Stock_holding.objects.filter(owner =request.user)
    stock_list = []
    for stock in stock_holding:
        stock_list.append({'name': stock.stock_info.name, 'y': stock.percentage})
    stock_data_dic = {'stock_list': stock_list}
    dataJSON = dumps(stock_data_dic)
    return render(request, 'myapp/stock_list.html',{
        "data": dataJSON,
    })