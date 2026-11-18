from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.CartAddAjaxView.as_view(), name='cart_add'),
    path('update/<int:product_id>/<str:action>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('clear/', views.CartClearView.as_view(), name='cart_clear'),
]
