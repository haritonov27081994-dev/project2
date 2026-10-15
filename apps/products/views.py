from django.shortcuts import render

def home_page_view(request):
    return render(request, template_name='products/index.html')

def product_list_view(request):
    products = [
        {"name": "Омега-3 Высокая концентрация", "brand": "Solgar", "description": "Для сердца и сосудов, 60 капсул", "price": 1800},
        {"name": "Витамин D3 5000 ME", "brand": "Now Foods", "description": "Для иммунитета и костей, 120 капсул", "price": 950},
    ]
    return render(request, template_name='products/product_list.html', context={'products': products})
