from django.db.models import Model
from django.shortcuts import render, get_object_or_404

from config.models import Product


def home(request):
    products = Product.objects.all()
    context = {'object_list': products}
    return render(request, 'home.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(
            f"Новая заявка на обратную связь:\nИмя: {name}\nТелефон: {phone}\nСообщение: {message}"
        )
    return render(request, 'contacts.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, **{'pk': pk})
    context = {'product': product}
    return render(request, 'product_details.html', context)
