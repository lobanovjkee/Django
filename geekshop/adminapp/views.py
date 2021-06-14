from django.contrib.auth.decorators import user_passes_test
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
    template_name = 'users.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'users.html', context=context)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'user_update.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'is_active', 'is_staff']
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context

    def get_success_url(self):
        return self.success_url


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {'title': title, 'update_form': user_form}
#
#     return render(request, 'user_update.html', context)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'user_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')
    # fields = '__all__'
    fields = ['first_name', 'last_name', 'avatar', 'age', 'is_active']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'user_update.html', context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'user_delete.html', context)

class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'categories.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'categories.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'categories_update.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

    def get_success_url(self):
        return self.success_url


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         form = ProductCategoryForm()
#
#     context = {
#         'title': title,
#         'form': form,
#     }
#
#     return render(request, 'categories_update.html', context)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'categories_update.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admin_staff:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


#
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST, request.FILES, instance=edit_category)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
#     else:
#         form = ProductCategoryForm(instance=edit_category)
#
#     context = {'title': title, 'form': form}
#
#     return render(request, 'categories_update.html', context)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'categories_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     context = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'categories_delete.html', context)

class ProductsListView(ListView):
    model = Product
    template_name = 'admin_products.html'
    context_object_name = 'objects'

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


#
# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'admin_products.html', context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'admin_products_update.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
#     else:
#         form = ProductForm()
#
#     context = {
#         'title': title,
#         'form': form,
#         'category': category,
#     }
#
#     return render(request, 'admin_products_update.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'admin_product_page.html'
    context_object_name = 'object'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {'title': title, 'object': product, }
#
#     return render(request, 'admin_product_page.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'admin_products_update.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['category'] = self.get_object().category
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:product_update', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#
#     edit_product = get_object_or_404(Product, id=pk)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=edit_product)
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
#     else:
#         form = ProductForm(instance=edit_product)
#
#     context = {
#         'title': title,
#         'form': form,
#         'category': edit_product.category,
#     }
#
#     return render(request, 'admin_products_update.html', context)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admin_product_delete.html'
    context_object_name = 'product_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        context['category'] = self.get_object().category
        return context

    def get_success_url(self):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return reverse_lazy('admin_staff:products', args=[self.object['category_id']])

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.is_active = False
    #     self.object.save()
    #
    #     return reverse_lazy('admin_staff:products', args=[self.object['category_id']])

# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))
#
#     context = {'title': title, 'product_to_delete': product}
#
#     return render(request, 'admin_product_delete.html', context)
