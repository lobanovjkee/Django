from django.shortcuts import render, get_object_or_404

import basketapp.views
from .models import Product, ProductCategory


def products(request, pk=None):
    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': 'каталог',
            'categories': categories,
            'category': category,
            'products': products,
            'total_quantity': basketapp.views.get_quantity(),
        }

        return render(request, 'products_list.html', content)


def product_page(request, pk=None):
    try:
        product = Product.objects.all()[pk - 1]
        context = {
            'title': product.name,
            'product': product,
            'total_quantity': basketapp.views.get_quantity(),
        }
        return render(request, 'product_page.html', context=context)
    except IndexError:
        return render(request, '404.html')
