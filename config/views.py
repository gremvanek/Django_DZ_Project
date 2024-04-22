import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, VersionForm
from .models import Product, Post, Version


class ContactView(TemplateView):
    template_name = 'contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(
            f"Новая заявка на обратную связь:\nИмя: {name}\nТелефон: {phone}\nСообщение: {message}"
        )
        return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PostView(TemplateView):
    template_name = 'create_post.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(
            f"Новая заявка на обратную связь:\nИмя: {name}\nТелефон: {phone}\nСообщение: {message}"
        )
        return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'object_list'  # Изменил context_object_name на 'object_list', чтобы избежать конфликта имен

    def get_queryset(self):
        queryset = super().get_queryset()
        published_posts = queryset.filter(is_published=True)
        return published_posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class PostCreateView(CreateView):
    model = Post
    template_name = 'create_view.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Вызываем метод родительского класса, чтобы сохранить данные формы и получить объект instance
        response = super().form_valid(form)

        # Генерируем случайный slug
        random_slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        counter = 1
        new_slug = random_slug
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = f"{random_slug}-{counter}"
            counter += 1

        # Сохраняем slug в экземпляре объекта Post
        instance.slug = new_slug
        instance.save()

        return response


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    context_object_name = 'post'
    slug_field = 'slug'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            active_version = product.version_set.filter(is_current=True).first()
            product.active_version = active_version
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_version = product.version_set.filter(is_current=True).first()
        context['active_version'] = active_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied
        return obj


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_success_url(self):
        return reverse_lazy('product_list')


class VersionListView(ListView):
    model = Version
    template_name = 'version_list.html'
    context_object_name = 'versions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение первого объекта Product
        product = Product.objects.first()

        # Если product не равен None, получаем идентификатор продукта (product_id)
        if product:
            product_id = product.pk
        else:
            product_id = None

        # Добавление идентификатора продукта в контекст
        context['product_id'] = product_id

        return context


class VersionDetailView(DetailView):
    model = Version
    template_name = 'version_detail.html'
    context_object_name = 'versions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = kwargs['product_id']
        return context


class VersionCreateView(CreateView):
    model = Version
    fields = ['product', 'version_number', 'version_name', 'is_current']
    template_name = 'version_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['product'] = self.kwargs['product_id']
        return initial


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    fields = ['product', 'version_number', 'version_name', 'is_current']
    template_name = 'version_form.html'

    def get_success_url(self):
        return reverse_lazy('versions')


class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version_confirm_delete.html'
    success_url = reverse_lazy('version_list')

    def get_success_url(self):
        return self.success_url
