from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from .models import ShopUser


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_link(user):
                print('сообщение для подтверждения регистрации отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения для подтверждения регистрации')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form,
    }

    return render(request, 'authapp/register.html', content)


@login_required()
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }

    return render(request, 'authapp/edit.html', context)


def send_verify_link(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = 'Account verification'
    message = f'Activate your account via this link: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == key and not user.is_activation_key_expires():
            print(f'user {user} is activated')
            user.is_active = True
            user.save()
            # auth.login(request, user)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'authapp/verify.html')
        else:
            print(f'key error activation user: {user}')
            return render(request, 'authapp/verify.html')

    except Exception as e:
        print(f'error activation user: {e.args}')

    return HttpResponseRedirect(reverse('index'))
