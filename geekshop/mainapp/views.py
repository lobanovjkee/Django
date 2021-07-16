import random

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_hot_product():
    products = Product.objects.all().select_related()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products


def products(request, pk=None, page=1):
    categories = ProductCategory.objects.all().select_related()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price').select_related()
            category = {
                'pk': 0,
                'name': 'все',
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price').select_related()

        paginator = Paginator(products, 3)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)

        context = {
            'title': 'каталог',
            'categories': categories,
            'category': category,
            'products': products_paginator,
            'hot_product': hot_product,
            'same_products': same_products,
            'paginator': paginator,
        }

        return render(request, 'mainapp/products_list.html', context)


def product_page(request, pk=None):
    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price').select_related()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price').select_related()
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': product.name,
        'product': product,
        'categories': categories,
        'category': category,
        'products': products,

    }
    return render(request, 'mainapp/product_page.html', context=context)


def product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse({'price': product.price})
