from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        # total_quantity = sum(item.quantity for item in basket)
        total_quantity = get_quantity()
        context = {
            'basket': basket,
            'total_quantity': total_quantity,
        }
        return render(request, 'basket.html', context)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk=None):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_quantity():
    basket = Basket.objects.all()
    total_quantity = sum(item.quantity for item in basket)

    return total_quantity
