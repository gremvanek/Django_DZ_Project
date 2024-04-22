import random

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import default_token_generator as token_generator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.utils import send_email_for_verify

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def get(self, request, *args, **kwargs):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # user = form.save()  # Сохраняем объект пользователя
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)  # Передаем запрос и пользователя в функцию
            return redirect('users:email_register')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/user_form.html'

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerifyView(View):
    success_url = reverse_lazy('users:login')

    @staticmethod
    def get(request, uidb64, token):
        try:
            # Decode uid and get the user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check token and user
        if user is not None and token_generator.check_token(user, token):
            # Set email_verified to True
            user.email_verified = True
            user.save()
            messages.success(request, "Your email has been successfully verified")
            return redirect('users:email_success')

        # If the token is invalid, show an error message
        messages.error(request, "The verification link is invalid or has expired")
        return redirect('users:email_fail')


class CustomPasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Генерация случайного пароля
        random_password = ''.join(
            random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
        # Хеширование пароля
        hashed_password = make_password(random_password)

        # Получение адреса электронной почты из формы
        email = form.cleaned_data['email']

        # Обновление пароля пользователя с указанным адресом электронной почты
        for user in form.get_users(email):
            user.set_password(hashed_password)
            user.save()

            # Отправка нового пароля на адрес электронной почты пользователя
            send_mail(
                _('Password reset'),
                _('Your new password is: {}').format(random_password),
                'from@example.com',
                [email],
                fail_silently=False,
            )

        # После успешного сброса пароля происходит редирект на страницу входа
        return super().form_valid(form)
