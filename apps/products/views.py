from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden  # Импортируем защиту доступа
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

# Финальный защищенный контроллер добавления товара на Django Forms
def product_add_view(request):
    # Проверяем безопасность: если не авторизован ИЛИ не админ — сразу блокируем
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут добавлять товары.</p>")

    # Если отправлена форма, передаем в нее данные из POST
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():  # Django автоматически запускает все проверки из формы!
            new_product = form.save()  # Автоматически создает товар в БД
            return redirect('products:product_detail', product_id=new_product.id)
    else:
        # Если GET-запрос — создаем пустую форму
        form = ProductForm()

    # Передаем форму в шаблон (при ошибках форма вернется с заполненными полями и текстом ошибок)
    return render(request, 'products/product_add.html', {'form': form})
