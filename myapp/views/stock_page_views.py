from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from ..models import Stock_change, Stock_holding, Stock_info, Stock_post
from ..forms import PostForm

def stock_page(request, code):
    stock_info = Stock_info.objects.get(code=code)
    page = request.GET.get('page', '1')
    post_list = Stock_post.objects.order_by('-create_date')
    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)
    context = {'post_list': page_obj, 'stock_name': stock_info.name}
    return render(request, "myapp/stock_page.html", context)

def post_create(request,code):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # author 속성에 로그인 계정 저장
            post.save()
            return redirect('myapp:stock-page/code')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'myapp/post_form.html', context)