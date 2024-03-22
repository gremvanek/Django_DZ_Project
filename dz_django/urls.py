from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import config
from config import views
from config.views import product_detail, ContactView, PostCreateView, PostDetailView, PostUpdateView, \
    PostDeleteView, PostListView

urlpatterns = [
                  path('', views.home, name='home'),
                  path('post_list/', PostListView.as_view(), name='post_list'),
                  path('contacts/', ContactView.as_view(), name='contacts'),
                  path('admin/', admin.site.urls),
                  path('product/<int:pk>/', product_detail, name='product_detail'),
                  path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
                  path('post_list/create/', PostCreateView.as_view(), name='create_view'),
                  path('<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
                  path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
