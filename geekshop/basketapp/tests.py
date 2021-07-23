from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket, BasketQuerySet


class BasketModelTest(TestCase):
    username = 'django'
    email = 'django@gb.local'
    password = 'geekbrains'
    status_code_success = 200
    status_code_redirect = 302

    def setUp(self):
        self.client = Client()
        self.user = ShopUser.objects.create_user(username=self.username, email=self.email, password=self.password)

        category_1 = ProductCategory.objects.create(name=f'category-1')
        self.product_1 = Product.objects.create(category=category_1, name='item-1', price=1000, quantity=2)
        self.product_2 = Product.objects.create(category=category_1, name='item-2', price=2000, quantity=3)
        self.product_3 = Product.objects.create(category=category_1, name='item-3', price=3000, quantity=5)

    def test_basket_model_str(self):
        basket = Basket.objects.create(
            user=self.user,
            product=self.product_1,
            quantity=3
        )
        self.assertEqual(str(basket), f'{basket.product.name} - {basket.quantity}')

    def test_basket_model_product_cost(self):
        basket = Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=2
        )
        self.assertEqual(basket.product_cost, basket.product.price * basket.quantity)

    def test_basket_model_get_items_cached(self):
        basket = Basket.objects.create(
            user=self.user,
            product=self.product_3,
            quantity=5
        )
        self.assertTrue(basket.get_items_cached, BasketQuerySet(basket))

    def test_basket_model_total_quantity(self):
        Basket.objects.create(
            user=self.user,
            product=self.product_3,
            quantity=5
        )
        Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=2
        )
        basket = Basket.objects.all().first()
        self.assertEqual(basket.total_quantity, sum(list(map(lambda x: x.quantity, Basket.objects.all()))))

    def test_basket_model_total_cost(self):
        Basket.objects.create(
            user=self.user,
            product=self.product_1,
            quantity=9
        )
        Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=4
        )
        basket = Basket.objects.all().first()
        self.assertEqual(basket.total_cost, sum(list(map(lambda x: x.product_cost, Basket.objects.all()))))

    def test_basket_model_get_item(self):
        Basket.objects.create(
            user=self.user,
            product=self.product_1,
            quantity=9
        )
        Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=4
        )
        Basket.objects.create(
            user=self.user,
            product=self.product_3,
            quantity=44
        )
        for basket in Basket.objects.all():
            self.assertEqual(basket.get_item(basket.pk), Basket.objects.get(pk=basket.pk))

    def test_basket_model_get_product(self):
        Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=4
        )
        Basket.objects.create(
            user=self.user,
            product=self.product_3,
            quantity=44
        )
        for basket in Basket.objects.all():
            self.assertTrue(
                basket.get_product(self.user, basket.product),
                Basket.objects.filter(user=self.user, product=basket.product)
            )

    def test_basket_model_delete(self):
        product_quantity = self.product_2.quantity
        basket = Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=3
        )
        self.assertEqual(self.product_2.quantity, product_quantity - basket.quantity)
        basket.delete()
        self.assertEqual(self.product_2.quantity, product_quantity)

    def test_basket_model_save(self):
        basket = Basket.objects.create(
            user=self.user,
            product=self.product_2,
            quantity=3
        )
        basket.save()
        if basket.pk:
            self.assertEqual(self.product_2.quantity,
                             basket.product.quantity - basket.quantity + Basket.objects.get(pk=basket.pk).quantity)
  