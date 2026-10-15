from django.urls import path
from . import views

app_name = 'products' # Пространство имен

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
]