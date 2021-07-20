import random

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    # _products = Product.objects.all().select_related()
    _products = get_products()

    return random.sample(list(_products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products


def products(request, pk=None, page=1):
    # categories = ProductCategory.objects.all().select_related()
    categories = get_links_menu()

    if pk is not None:
        if pk == 0:
            # _products = Product.objects.all().order_by('price').select_related()
            _products = get_products_ordered_by_price()
            category = {
                'pk': 0,
                'name': 'все',
            }
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            # _products = Product.objects.filter(category__pk=pk).order_by('price').select_related()
            _products = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(_products, 3)

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
    # categories = ProductCategory.objects.all()
    categories = get_links_menu()

    if pk is not None:
        if pk == 0:
            # _products = Product.objects.all().order_by('price').select_related()
            _products = get_products_ordered_by_price()

            category = {'name': 'все'}
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            # _products = Product.objects.filter(category__pk=pk).order_by('price').select_related()
            _products = get_products_in_category_ordered_by_price(pk)
    product = get_product(pk)
    context = {
        'title': product.name,
        'product': product,
        'categories': categories,
        'category': category,
        'products': _products,

    }
    return render(request, 'mainapp/product_page.html', context=context)


def product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse({'price': product.price})
