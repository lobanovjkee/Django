from django.shortcuts import render

from mainapp.models import Product
from mainapp.views import get_products


def main(request):
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    products = get_products()[:3]
    context = {
        "title": 'магазин',
        'topic': 'тренды',
        'products': products,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    context = {
        'title': 'контакты',
    }
    return render(request, 'geekshop/contact.html', context=context)
