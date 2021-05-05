from django.shortcuts import render
from .models import Product


def products(request):
    context = {
        'title': 'каталог',
        'links': [
            {'href': 'mainapp:products', 'name': 'все'},
            {'href': 'mainapp:products', 'name': 'дом'},
            {'href': 'mainapp:products', 'name': 'офис'},
            {'href': 'mainapp:products', 'name': 'модерн'},
            {'href': 'mainapp:products', 'name': 'классика'}
        ]}

    return render(request, 'products.html', context=context)


def product_page(request, pk=None):
    try:
        product = Product.objects.all()[pk - 1]

        context = {
            'product': product,

        }
        return render(request, 'product_page.html', context=context)
    except IndexError:
        return render(request, '404.html')
