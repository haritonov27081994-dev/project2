from django.shortcuts import render
from .models import Product


def home_page_view(request):
    products = Product.objects.all()
    return render(request, template_name='products/index.html', context={'products': products})