from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


def home_page_view(request):
    return render(request, template_name='products/index.html')


def product_list_view(request):
    # На витрине показываем только одобренные (опубликованные) товары
    products = Product.objects.filter(status='published').order_by('-created_at')
    return render(request, template_name='products/product_list.html', context={'products': products})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Если товар еще не опубликован, его может смотреть только продавец или администратор
    if product.status != 'published':
        if not request.user.is_authenticated or (product.seller != request.user and not request.user.is_staff):
            return HttpResponseForbidden("<h1>Товар недоступен</h1><p>Этот товар находится на проверке или отклонен модератором.</p>")

    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_add_view(request):
    extra_context = {
        "title": "Добавить новый товар",
        "h1": "Добавление БАДа в каталог",
        "submit_button_text": "Отправить на проверку",
    }

    if request.method == "POST":
        # Обязательно передаем request.FILES для загрузки картинки!
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller = request.user
            new_product.status = 'pending'  # Новый товар идет на проверку
            new_product.save()
            return redirect('users:profile')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', context={"form": form, **extra_context})


@login_required
def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user and not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Вы можете редактировать только свои товары.</p>")

    extra_context = {
        "title": "Редактировать товар",
        "h1": "Редактирование БАДа",
        "submit_button_text": "Сохранить изменения",
    }

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            # Если редактирует обычный продавец (не админ), отправляем товар на повторную проверку
            if not request.user.is_staff:
                updated_product.status = 'pending'
            updated_product.save()
            return redirect("products:product_detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', context={"form": form, **extra_context})


@login_required
def product_remove_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user and not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Вы можете удалять только свои товары.</p>")

    if request.method == "POST":
        product.delete()
        return redirect("users:profile")

    return render(request, 'products/product_remove_confirm.html', {'product': product})
