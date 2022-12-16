from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from .forms import StockForm
from .models import Stock


@csrf_exempt
def index(request, stock=""):
    if request.method == 'GET':
        form = StockForm()
        stock_list = Stock.objects.all()
        total_amount = get_total_amount(stock_list)
        print(stock_name_to_price('제넥신'))
        return render(request, 'myapp/index.html', {
            "form": form,
            "total_amount": total_amount,
            "stock_list": stock_list
        })
        
    elif request.method == 'POST':
        form = StockForm(request.POST)

        if form.is_valid():
            stock = Stock(
                stock_name=form.cleaned_data['stock_name'],
                stock_amount=form.cleaned_data['stock_amount']
            )
            stock.save()
            return HttpResponseRedirect("/")

def get_total_amount(stock_list):
    stock_kinds = []
    total_amount = []
    for stock in stock_list:
            if stock.stock_name not in stock_kinds:
                stock_kinds.append(stock.stock_name)
    for stock in stock_kinds:
        total_amount.append([stock, stock_name_to_price(stock) ,Stock.objects.filter(
            stock_name=stock).aggregate(Sum('stock_amount'))])
    return total_amount
        

def stock_name_to_code(name):
    df = pd.read_csv("https://raw.githubusercontent.com/cosmos1030/beautifulsoup-study/main/data/nameToCode.csv")
    df.set_index('종목명', inplace = True)
    code = df.loc[name][0]
    return code

def stock_code_to_price(code):
    page = requests.get("https://finance.naver.com/item/main.naver?code="+code)
    soup = bs(page.text, "html.parser")
    element = soup.select_one('#chart_area > div.rate_info > div > p.no_today > em > .blind')
    price = element.get_text()
    return price

def stock_name_to_price(name):
    code = stock_name_to_code(name)
    price = stock_code_to_price(code)
    return price