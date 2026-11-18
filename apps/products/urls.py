from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:product_id>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:product_id>/remove/', views.ProductDeleteView.as_view(), name='product_remove'),
    path('products/<int:product_id>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
