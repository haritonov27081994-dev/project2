from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden  # Импортируем защиту доступа
from .models import Product

def home_page_view(request):
    return render(request, template_name='products/index.html')

def product_list_view(request):
    products = Product.objects.all() 
    return render(request, template_name='products/product_list.html', context={'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# Финальный защищенный контроллер добавления товара
def product_add_view(request):
    # Проверяем: если не авторизован ИЛИ не является админом (персоналом)
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут добавлять товары.</p>")

    # Если это админ, отдаем форму или принимаем данные
    if request.method == "GET":
        return render(request, 'products/product_add.html')
        
    elif request.method == "POST":
        new_product = Product.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            description=request.POST['description']
        )
        return redirect('products:product_detail', product_id=new_product.id)