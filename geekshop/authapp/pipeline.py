from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max_orig&access_token={response['access_token']}&v=5.131"
    vk_response = requests.get(api_url)

    if vk_response.status_code != 200:
        return

    vk_data = vk_response.json()['response'][0]
    if vk_data['sex']:
        if vk_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif vk_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if vk_data['about']:
        user.shopuserprofile.about_me = vk_data['about']

    if vk_data['bdate']:
        b_date = datetime.strptime(vk_data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - b_date.year - (
                (timezone.now().date().month, timezone.now().date().day) < (b_date.month, b_date.day))

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if vk_data['photo_max_orig']:
        photo = requests.get(vk_data['photo_max_orig']).content
        user_photo_path = f'user_avatars/{user.username}_photo.jpg'

        with open(f'{settings.MEDIA_ROOT}/{user_photo_path}', 'wb') as f:
            f.write(photo)

        user.avatar = user_photo_path

    user.save()
