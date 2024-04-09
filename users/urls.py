from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailVerifyView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/', TemplateView.as_view(template_name='users/email_register.html'), name='email_register'),
    path('confirm_email/success/', TemplateView.as_view(template_name='users/confirm_email_success.html'), name='email_success'),
    path('confirm_email/fail/', TemplateView.as_view(template_name='users/confirm_email_fail.html'), name='email_fail'),
    path('confirm_email/<uidb64>/<token>/', EmailVerifyView.as_view(), name='confirm_email'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
