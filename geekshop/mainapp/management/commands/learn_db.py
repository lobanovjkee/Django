from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        action_1 = 1
        action_2 = 2
        action_expired = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated_at__lte=F('order__created_at') + action_1__time_delta)

        action_2__condition = Q(order__updated_at__gt=F('order__created_at') + action_1__time_delta) & Q(
            order__updated_at__lte=F('order__created_at') + action_2__time_delta)

        action_expired__condition = Q(order__updated_at__gt=F('order__created_at') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=action_1)
        action_2__order = When(action_2__condition, then=action_2)
        action_expired__order = When(action_expired__condition, then=action_expired)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for order_item in test_orders:
            print(f'{order_item.action_order:2}: заказ №{order_item.pk:3}:\
                   {order_item.product.name:15}: скидка\
                   {abs(order_item.total_price):6.2f} руб. | \
                   {order_item.order.updated_at - order_item.order.created_at}')
