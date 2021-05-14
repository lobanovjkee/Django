from django.shortcuts import render

import basketapp.views
from mainapp.models import Product


def main(request):
    products = Product.objects.all()[:4]
    context = {
        "title": 'магазин',
        'topic': 'тренды',
        'products': products,
        'total_quantity': basketapp.views.get_quantity(),
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    context = {
        'title': 'контакты',
        'total_quantity': basketapp.views.get_quantity(),
    }
    return render(request, 'contact.html', context=context)
