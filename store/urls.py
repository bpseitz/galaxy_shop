from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products'),
    path('products/<int:product_id>', views.show_product, name='product'),
    path('cart', views.show_cart, name="cart"),
    path('products/new', views.new),
    path('products/create', views.create),
    path('products/<int:product_id>/upload', views.upload),
]