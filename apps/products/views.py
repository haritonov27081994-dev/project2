from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Category, Product
from .forms import ProductForm


class HomePageView(TemplateView):
    template_name = 'products/index.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(status='published').order_by('-created_at')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.current_category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.current_category)
        else:
            self.current_category = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = getattr(self, 'current_category', None)
        return context


class ProductDetailView(UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def test_func(self):
        product = self.get_object()
        if product.status == 'published':
            return True
        user = self.request.user
        return user.is_authenticated and (product.seller == user or user.is_staff)

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if self.request.user.is_authenticated:
            product.viewed_by_users.add(self.request.user)
        return product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить новый товар"
        context['h1'] = "Добавление БАДа в каталог"
        context['submit_button_text'] = "Отправить на проверку"
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.status = 'pending'
        messages.success(self.request, "Товар успешно добавлен и отправлен на проверку!")
        return super().form_valid(form)


class SellerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return product.seller == self.request.user or self.request.user.is_staff


class ProductUpdateView(SellerOrStaffMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактировать товар"
        context['h1'] = "Редактирование БАДа"
        context['submit_button_text'] = "Сохранить изменения"
        return context

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.status = 'pending'
        messages.success(self.request, "Изменения товара успешно сохранены!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'product_id': self.object.id})


class ProductDeleteView(SellerOrStaffMixin, DeleteView):
    model = Product
    template_name = 'products/product_remove_confirm.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, f'Товар «{self.object.title}» удален.')
        return super().form_valid(form)


class ToggleFavoriteView(LoginRequiredMixin, View):
    """Добавление или удаление товара из избранного с выводом messages.success."""
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user in product.favorited_by.all():
            product.favorited_by.remove(request.user)
            messages.info(request, f'Товар «{product.title}» удален из избранного.')
        else:
            product.favorited_by.add(request.user)
            messages.success(request, f'Товар «{product.title}» успешно добавлен в избранное!')

        # Возвращаем пользователя на ту же страницу, где он нажал кнопку
        next_url = request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('products:product_detail', product_id=product.id)
