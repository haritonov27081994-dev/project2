import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from apps.products.models import Product


class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids)

        cart_items = []
        total_price = Decimal('0.00')

        for product in products:
            quantity = cart.get(str(product.id), 0)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context


class CartAddAjaxView(View):
    """Обработчик AJAX-запросов от JavaScript при нажатии 'Добавить в корзину'."""
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, status='published')
        cart = request.session.get('cart', {})
        pid_str = str(product.id)

        cart[pid_str] = cart.get(pid_str, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True

        total_items = sum(cart.values())

        return JsonResponse({
            'status': 'ok',
            'product_title': product.title,
            'product_qty': cart[pid_str],
            'total_items': total_items,
            'message': f'Товар «{product.title}» добавлен в корзину!'
        })


class CartUpdateView(View):
    """Увеличение, уменьшение или удаление позиции на странице самой корзины."""
    def post(self, request, product_id, action):
        cart = request.session.get('cart', {})
        pid_str = str(product_id)

        if pid_str in cart:
            if action == 'increase':
                cart[pid_str] += 1
            elif action == 'decrease':
                cart[pid_str] -= 1
                if cart[pid_str] <= 0:
                    del cart[pid_str]
            elif action == 'remove':
                del cart[pid_str]

            request.session['cart'] = cart
            request.session.modified = True

        return redirect('cart:cart_detail')


class CartClearView(View):
    """Полная очистка корзины."""
    def post(self, request):
        request.session['cart'] = {}
        request.session.modified = True
        messages.info(request, 'Корзина очищена.')
        return redirect('cart:cart_detail')
