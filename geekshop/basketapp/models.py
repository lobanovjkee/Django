from django.db import models

from geekshop import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super().delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user).select_related()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user).select_related()
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        super().save(*args, **kwargs)
