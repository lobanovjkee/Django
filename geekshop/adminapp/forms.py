from django import forms
from django.forms import ModelForm
from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryForm(ModelForm):
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name in ['discount', 'is_active']:
                field.widget.attrs['class'] = ''


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
