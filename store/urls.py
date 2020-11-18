from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products'),
    path('products/<int:product_id>', views.show_product, name='product'),
    path('cart', views.show_cart, name="cart"),
]