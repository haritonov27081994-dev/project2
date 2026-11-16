from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
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


@login_required
def product_add_view(request):
    extra_context = {
        "title": "Добавить новый товар",
        "h1": "Добавление БАДа в каталог",
        "submit_button_text": "Опубликовать на витрине",
    }

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)  # Создаем объект, но пока не пишем в БД
            new_product.author = request.user      # Привязываем товар к текущему пользователю
            new_product.save()                     # Сохраняем в БД
            return redirect('products:product_detail', product_id=new_product.id)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', context={"form": form, **extra_context})


@login_required
def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, что редактирует автор товара или администратор
    if product.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Вы можете редактировать только свои товары.</p>")

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


@login_required
def product_remove_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, что удаляет автор товара или администратор
    if product.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Вы можете удалять только свои товары.</p>")

    if request.method == "POST":
        product.delete()
        return redirect("products:product_list")

    return render(request, 'products/product_remove_confirm.html', {'product': product})
