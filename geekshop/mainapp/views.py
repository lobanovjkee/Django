import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products


def products(request, pk=None, page=1):
    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {
                'pk': 0,
                'name': 'все',
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)

        content = {
            'title': 'каталог',
            'categories': categories,
            'category': category,
            'products': products_paginator,
            'basket': get_basket(request.user),
            'hot_product': hot_product,
            'same_products': same_products,
        }

        return render(request, 'products_list.html', content)


def product_page(request, pk=None):
    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': product.name,
        'product': product,
        'categories': categories,
        'category': category,
        'products': products,
        'basket': get_basket(request.user),
    }
    return render(request, 'product_page.html', context=context)
