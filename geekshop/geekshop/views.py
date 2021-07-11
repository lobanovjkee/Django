from django.shortcuts import render

from mainapp.models import Product


def main(request):
    products = Product.objects.all()[:4]
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
