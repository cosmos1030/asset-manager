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
        stock_change = Stock.objects.all()
        stock_list = get_total_amount(stock_change)
        total_total_price = get_total_total_price(stock_list)
        return render(request, 'myapp/index.html', {
            "form": form,
            "stock_list": stock_list,
            "stock_change": stock_change,
            "total_total_price": total_total_price
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

def get_total_amount(stock_change):
    stock_kinds = []
    total_amount = []
    for stock in stock_change:
            if stock.stock_name not in stock_kinds:
                stock_kinds.append(stock.stock_name)
    for stock in stock_kinds:
        stock_price = stock_name_to_price(stock)
        stock_amount = Stock.objects.filter(stock_name=stock).aggregate(Sum('stock_amount'))['stock_amount__sum']
        total_price = stock_price * stock_amount
        total_amount.append([stock, stock_price, stock_amount, total_price])
    return total_amount

def get_total_total_price(total_amount):
    total_total_price = 0
    for stock_info in total_amount:
        total_total_price += stock_info[3]
    return total_total_price


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
    price = int(price.replace(',', ''))
    return price