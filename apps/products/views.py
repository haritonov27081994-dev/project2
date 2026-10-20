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
        if form.is_valid():  # Django автоматически запускает все проверки из формы
            new_product = form.save()  # Автоматически создает товар в БД
            return redirect('products:product_detail', product_id=new_product.id)
    else:
        # Если GET-запрос — создаем пустую форму
        form = ProductForm()

    # Передаем форму в шаблон (при ошибках форма вернется с заполненными полями и текстом ошибок)
    return render(request, 'products/product_add.html', {'form': form})


# НОВЫЙ защищенный контроллер редактирования товара на базе ModelForm с урока
def product_edit_view(request, product_id):
    # Проверяем безопасность: редактировать каталог могут только администраторы
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут редактировать товары.</p>")

    # Получаем существующий БАД из базы данных или отдаем ошибку 404
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        # Передаем измененные данные из POST и связываем их с редактируемым БАДом через instance
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()  # Django обновит текущую запись в базе данных (выполнит SQL UPDATE)
            return redirect("products:product_detail", product_id=product.id)
        # Если в форме допущены ошибки — возвращаем страницу редактирования со списком ошибок
        return render(request, 'products/product_edit.html', context={"form": form})

    # При GET-запросе создаем форму, автоматически предзаполненную текущими данными этого БАДа
    form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', context={"form": form})
