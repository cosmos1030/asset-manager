from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request, stock=""):
    if request.method == 'GET':
	    return render(request, 'myapp/index.html')
    elif request.method == 'POST':
        stock_name = request.POST['stock_name']
        stock_amount = request.POST['stock_amount']
        return render(request, 'myapp/index.html', {'stock': stock_name})