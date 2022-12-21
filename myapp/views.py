from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from .forms import StockChangeForm
from .models import Stock_change, Stock_holding


@csrf_exempt
def index(request, stock=""):
    if request.method == 'GET':
        form = StockChangeForm()
        stock_holding = Stock_holding.objects.all()
        stock_change = Stock_change.objects.all()
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
            # 변동 내역에 추가
            stock_change = Stock_change(
                name=form.cleaned_data['name'],
                amount=form.cleaned_data['amount']
            )
            stock_change.save()

            # 주식 보유 현황에 추가
            stock_holding = Stock_holding.objects.get(stock.name=stock_change.name)
            stock_holding.amount += stock_change.amount
            stock_holding.save()
            return HttpResponseRedirect("/")

def get_total_asset(stock_holding):
    t
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