from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import config
from config import views

urlpatterns = [
                  path('', views.home, name='home'),
                  path('contacts/', views.contacts, name='contacts'),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
