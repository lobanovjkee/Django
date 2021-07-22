from authapp.models import ShopUser
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q
from adminapp.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_users = ShopUser.objects.filter(
            Q(is_active=True) |
            Q(activation_key__isnull=True)
        )

        for _id, user in enumerate(active_users):
            print(f'{_id}:{user.first_name} {user.last_name} - {user.email}')

        db_profile_by_type('active_users', '', connection.queries)
