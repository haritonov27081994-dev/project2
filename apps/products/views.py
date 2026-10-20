from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden  
from django.views.decorators.http import require_POST  # Импортируем декоратор из урока
from .models import Product
from .forms import ProductForm 

def home_page_view(request):
    return render(request, template_name='products/index.html')

def product_list_view(request):
    products = Product.objects.all() 
    return render(request, template_name='products/product_list.html', context={'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# Универсальный контроллер добавления товара
def product_add_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут добавлять товары.</p>")

    extra_context = {
        "title": "Добавить новый товар",
        "h1": "Добавление БАДа в каталог",
        "submit_button_text": "Опубликовать на витрине",
    }

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            return redirect('products:product_detail', product_id=new_product.id)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', context={"form": form, **extra_context})

# Универсальный контроллер редактирования товара
def product_edit_view(request, product_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут редактировать товары.</p>")

    product = get_object_or_404(Product, id=product_id)

    extra_context = {
        "title": "Редактировать товар",
        "h1": "Редактирование БАДа",
        "submit_button_text": "Сохранить изменения",
    }

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:product_detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', context={"form": form, **extra_context})

# НОВЫЙ защищенный контроллер удаления товара с декоратором require_POST
@require_POST
def product_remove_view(request, product_id):
    # Двойная защита: даже если POST-запрос отправлен в обход интерфейса, проверяем права
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут удалять товары.</p>")
        
    # Находим БАД и удаляем его из базы данных
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    
    # После успешного удаления перенаправляем админа на общий каталог товаров
    return redirect("products:product_list")
