from django.db.models import Model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView
import random
import string
from config.models import Product, Post


def home(request):
    products = Product.objects.all()
    context = {'object_list': products}
    return render(request, 'home.html', context)


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

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)


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
    # context_object_name = 'posts' - из-за этой строки падал post_list с ошибкой - 'Post' object is not iterable

    def get_queryset(self):
        queryset = super().get_queryset()
        published_posts = queryset.filter(is_published=True)
        # unpublished_posts = queryset.filter(is_published=False)
        return published_posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1  # Увеличиваем счетчик просмотров на 1
        obj.save()  # Сохраняем изменения
        return obj


class PostCreateView(CreateView):
    model = Post
    template_name = 'create_view.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Генерируем случайное число или символ в качестве Slug
        random_slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        # Проверяем уникальность Slug, добавляя уникальный идентификатор, если необходимо
        counter = 1
        new_slug = random_slug
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = f"{random_slug}-{counter}"
            counter += 1

        # Сохраняем Slug в объекте статьи
        instance.slug = new_slug

        instance.save()
        return super().form_valid(form)


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


def product_detail(request, pk):
    product = get_object_or_404(Product, **{'pk': pk})
    product.increment_views()  # increment для добавления просмотров
    context = {'product': product}
    return render(request, 'product_details.html', context)
