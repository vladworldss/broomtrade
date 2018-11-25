from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from .models import Category,Good


def index(request, cat_id):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1
    cats = Category.objects.all().order_by('name')
    if not cat_id:
        cat = Category.objects.first()
    else:
        cat = Category.objects.get(pk=cat_id)
    # make pagination
    pag = Paginator(Good.objects.filter(category=cat).order_by('name'), 2)
    try:
        goods = pag.page(page_num)
    except InvalidPage:
        goods = pag.page(1)

    return render(request, 'index.html',
                  {'category': cat, 'cats': cats, 'goods': goods}
                  )


def good(request, good_id):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1
    cats = Category.objects.all().order_by('name')
    try:
        good = Good.objects.get(pk=good_id)
    except Good.DoesNotExist:
        raise Http404
    return render(request, 'good.html', {'cats': cats, 'good': good, 'pn': page_num})
