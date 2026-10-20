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

# Оптимизированный контроллер добавления товара
def product_add_view(request):
    # Проверяем безопасность: если не авторизован ИЛИ не админ — сразу блокируем
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут добавлять товары.</p>")

    # Инициализируем переменные для контекста (понадобятся для GET или при ошибках POST)
    context = {}

    # Обрабатываем отправку формы
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()

        errors = {}

        # Валидация полей
        if not title:
            errors['title'] = 'Название БАДа обязательно к заполнению.'
        elif len(title) < 3:
            errors['title'] = 'Название должно содержать не менее 3 символов.'
        
        if not description:
            errors['description'] = 'Описание и состав добавки обязательны к заполнению.'
        
        if not price:
            errors['price'] = 'Укажите цену товара.'
        else:
            try:
                float_price = float(price)
                if float_price <= 0:
                    errors['price'] = 'Цена должна быть больше нуля.'
            except ValueError:
                errors['price'] = 'Цена должна быть числом.'

        # Если ошибок нет — создаем БАД и делаем редирект
        if not errors:
            new_product = Product.objects.create(
                title=title,
                price=price,
                description=description
            )
            return redirect('products:product_detail', product_id=new_product.id)
        
        # Если ошибки есть — наполняем контекст данными, чтобы они вернулись в форму
        context = {
            'errors': errors,
            'title': title,
            'description': description,
            'price': price,
        }

    # Этот рендер сработает по умолчанию: 
    # 1. При GET-запросе (с пустым контекстом)
    # 2. При POST-запросе с ошибками (с контекстом, содержащим ошибки и введенный текст)
    return render(request, 'products/product_add.html', context)
