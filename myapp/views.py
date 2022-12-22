from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from .forms import StockChangeForm
from .models import Stock_change, Stock_holding, Stock_info


@csrf_exempt
def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("common/login/")
    if request.method == 'GET':
        form = StockChangeForm()
        stock_holding = Stock_holding.objects.filter(owner =request.user)
        stock_change = Stock_change.objects.filter(owner =request.user)
        total_asset = get_total_asset(stock_holding)
        return render(request, 'myapp/index.html', {
            "form": form,
            "stock_holding": stock_holding,
            "stock_change": stock_change,
            "total_asset": total_asset
        })
        
    elif request.method == 'POST':
        form = StockChangeForm(request.POST)

        if form.is_valid():
            name=form.cleaned_data['name']
            amount=form.cleaned_data['amount']

            # 변동 내역에 추가
            stock_change = Stock_change(
                owner = request.user,
                name=name,
                amount=amount
            )
            stock_change.save()

            # 주식 정보 반영
            stock_info = get_stock_info(name)

            # 주식 보유 현황에 반영
            stock_holding = get_stock_holding(stock_info, amount, request.user)
            return HttpResponseRedirect("/")

def get_total_asset(stock_holding):
    total_asset = 0
    for stock in stock_holding:
        total_asset += stock.total_price
    return total_asset

def get_stock_info(name):
    code = stock_name_to_code(name)
    price = stock_code_to_price(code)
    price = int(price.replace(',', ''))
    try:
        stock_info = Stock_info.objects.get(name=name)
        stock_info.price = price
    except:
        stock_info = Stock_info(name=name, code=code, current_price= price)
    stock_info.save()
    return stock_info

def get_stock_holding(stock_info, amount, user):
    added_price = stock_info.current_price * amount
    try:
        stock_holding = Stock_holding.objects.get(stock_info__name = stock_info.name, owner=user)
        stock_holding.amount += amount
        stock_holding.total_price += added_price
    except:
        print('except')
        stock_holding = Stock_holding(owner=user ,stock_info=get_stock_info(stock_info.name), amount = amount, total_price= added_price)
    stock_holding.save()
    return stock_holding


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

