from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView

from adminapp.forms import ProductCategoryForm, ProductForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404
from mainapp.models import Product, ProductCategory


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'is_active', 'is_staff']
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context

    def get_success_url(self):
        return self.success_url


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'
    fields = ['first_name', 'last_name', 'avatar', 'age', 'is_active']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

    def get_success_url(self):
        return self.success_url


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admin_staff:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/categories_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        # for item in Product.objects.filter(category=self.object):
        #     item.is_active = False
        #     item.save()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/admin_products.html'
    context_object_name = 'objects'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукт'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__pk=self.kwargs.get('pk')).order_by('name')
        return queryset

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/admin_products_update.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.kwargs['pk']])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/admin_product_page.html'
    context_object_name = 'object'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/admin_products_update.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['category'] = self.get_object().category
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:product_update', args=[self.kwargs['pk']])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/admin_product_delete.html'
    context_object_name = 'product_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        context['category'] = self.get_object().category
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(reverse_lazy('admin_staff:categories'))
