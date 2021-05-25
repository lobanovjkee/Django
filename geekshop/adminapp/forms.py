from django.forms import ModelForm
from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
