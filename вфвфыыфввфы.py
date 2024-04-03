import random
import string

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, Post  # Обратите внимание, что здесь я изменяю импорт моделей


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

    # context_object_name = 'object_list'  # Изменил context_object_name на 'object_list', чтобы избежать конфликта имен

    def get_queryset(self):
        queryset = super().get_queryset()
        published_posts = queryset.filter(is_published=True)
        return published_posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
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


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_success_url(self):
        return reverse_lazy('product_list')
