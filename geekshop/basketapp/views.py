from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    if request.user.is_authenticated:
        _basket = Basket.objects.filter(user=request.user)
        context = {
            'basket': _basket,

        }
        return render(request, 'basketapp/basket.html', context)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    _basket = Basket.objects.filter(user=request.user, product=product).first()

    if not _basket:
        _basket = Basket(user=request.user, product=product)

    _basket.quantity += 1
    _basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk=None):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        _basket = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket': _basket,
        }

        result = render_to_string('includes/inc_table.html', content)

        return JsonResponse({'result': result})
