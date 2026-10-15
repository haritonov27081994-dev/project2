from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
]