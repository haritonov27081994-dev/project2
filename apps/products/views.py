from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Category, Product
from .forms import ProductForm


class HomePageView(TemplateView):
    template_name = 'products/index.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 6  # Пагинация: по 6 товаров на одной странице

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
        # Если пользователь вошел в аккаунт — записываем его в список просмотревших
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
        return super().form_valid(form)


class SellerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин проверки прав: редактировать и удалять может только продавец товара или админ."""
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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'product_id': self.object.id})


class ProductDeleteView(SellerOrStaffMixin, DeleteView):
    model = Product
    template_name = 'products/product_remove_confirm.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('users:profile')
