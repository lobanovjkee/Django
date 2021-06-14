from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_products')
def media_folder_products(string):
    if not string:
        string = 'products_images/default.png'
    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'user_avatars/default_avatar.svg'
    return f'{settings.MEDIA_URL}{string}'


