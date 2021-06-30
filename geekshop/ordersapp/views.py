from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ordersapp.models import Order


class OrderList(ListView):
    model = Order
    template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrder(CreateView):
    pass


class UpdateOrder(UpdateView):
    pass


class DeleteOrder(DeleteView):
    pass


class ReadOrder(DetailView):
    pass


def forming_complete(request, pk):
    pass
