from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser


class UserManagementTest(TestCase):
    username = 'django'
    superuser_username = 'admin'
    wrong_username = 'notdjango'
    email = 'django@local.gb'
    superuser_email = 'admin@local.gb'
    password = 'geekbrains'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username': 'Valid',
        'first_name': 'Django',
        'last_name': 'Django',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'valid@gb.local',
        'age': 26,
    }

    new_under_age_user_data = {
        'username': 'Invalid',
        'first_name': 'Django',
        'last_name': 'Django',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'invalid@gb.local',
        'age': 17,
    }

    def setUp(self):
        self.user = ShopUser.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.superuser = ShopUser.objects.create_superuser(username=self.superuser_username, email=self.superuser_email,
                                                           password=self.password)
        self.client = Client()

    def test_user_flow(self):
        self._test_user_login(self.username, self.password)
        self._test_user_logout()

        self._test_wrong_login_credentials(self.wrong_username, self.password)

    def is_anonymous(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

    def is_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_authenticated)

    def _test_user_login(self, username, password):
        self.is_anonymous()

        self.client.login(username=username, password=password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_code_redirect)

        self.is_authenticated()

    def _test_wrong_login_credentials(self, username, password):
        self.is_anonymous()

        self.client.login(username=username, password=password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_code_success)

    def _test_user_logout(self):
        self.is_authenticated()

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        self.is_anonymous()

    def register_start(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_register_valid_user(self):
        self.register_start()

        response = self.client.post('/auth/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)
        new_user = ShopUser.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user.email}/{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def test_register_invalid_user(self):
        self.register_start()

        response = self.client.post('/auth/register/', data=self.new_under_age_user_data)
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertRaises(ValidationError)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')
