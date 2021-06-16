from django.urls import path
from .views import products, product_page

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', product_page, name='product_page'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('category/<int:pk>/', products, name='category'),

]
