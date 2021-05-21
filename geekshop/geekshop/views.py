from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def main(request):
    products = Product.objects.all()[:4]
    basket = ''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        "title": 'магазин',
        'topic': 'тренды',
        'products': products,
        'basket': basket,
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    basket = ''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': 'контакты',
        'basket': basket,
    }
    return render(request, 'contact.html', context=context)
