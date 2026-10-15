from django.shortcuts import render, get_object_or_404
from .models import Product

def home_page_view(request):
    return render(request, template_name='products/index.html')

def product_list_view(request):

    products = Product.objects.all() 
    return render(request, template_name='products/product_list.html', context={'products': products})

def product_detail_view(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
