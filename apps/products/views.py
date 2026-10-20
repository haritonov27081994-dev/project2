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

# Защищенный контроллер добавления товара с полной валидацией
def product_add_view(request):
    # Проверяем: если не авторизован ИЛИ не является админом (персоналом)
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("<h1>Доступ запрещен</h1><p>Только администраторы могут добавлять товары.</p>")

    if request.method == "GET":
        return render(request, 'products/product_add.html')
        
    elif request.method == "POST":
        # Получаем данные из формы и очищаем от случайных пробелов по краям
        title = request.POST.get('title', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()

        errors = {}

        # 1. Валидация названия (обязательное поле + не менее 3 символов)
        if not title:
            errors['title'] = 'Название БАДа обязательно к заполнению.'
        elif len(title) < 3:
            errors['title'] = 'Название должно содержать не менее 3 символов.'
        
        # 2. Валидация описания
        if not description:
            errors['description'] = 'Описание и состав добавки обязательны к заполнению.'
        
        # 3. Валидация цены (проверка на пустоту, на число и на значение > 0)
        if not price:
            errors['price'] = 'Укажите цену товара.'
        else:
            try:
                float_price = float(price)
                if float_price <= 0:
                    errors['price'] = 'Цена должна быть больше нуля.'
            except ValueError:
                errors['price'] = 'Цена должна быть числом.'

        # Если в словаре errors есть ошибки — возвращаем форму с сохраненным вводом
        if errors:
            context = {
                'errors': errors,
                'title': title,
                'description': description,
                'price': price,
            }
            return render(request, 'products/product_add.html', context)

        # Если все проверки пройдены успешно — создаем БАД в базе данных
        new_product = Product.objects.create(
            title=title,
            price=price,
            description=description
        )
        return redirect('products:product_detail', product_id=new_product.id)