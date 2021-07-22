from django.test import TestCase
from django.test.client import Client
from mainapp.models import ProductCategory, Product


class MainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self):
        category_1 = ProductCategory.objects.create(name=f'category-1')
        for i in range(100):
            Product.objects.create(
                category=category_1,
                name=f'item-{i}'
            )
        self.client = Client()

    def test_index_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_contacts_url(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_show_all_products_url(self):
        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_product_categories_urls(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/{product.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_login_url(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_code_success)
