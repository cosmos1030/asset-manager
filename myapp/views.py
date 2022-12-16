from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import StockForm
from .models import Stock

@csrf_exempt
def index(request, stock=""):
    if request.method == 'GET':
        form = StockForm()
        stock_list = Stock.objects.all()
        return render(request, 'myapp/index.html', {
            "form": form,
            "stock_list": stock_list
        })
    elif request.method == 'POST':
        form = StockForm(request.POST)

        if form.is_valid():
            stock = Stock(
                stock_name = form.cleaned_data['stock_name'],
                stock_amount = form.cleaned_data['stock_amount']
            )
            stock.save()
            return HttpResponseRedirect("/")