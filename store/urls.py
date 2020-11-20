from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('products/<int:product_id>', views.show_product),
    path('cart', views.show_cart),
    path('products/new', views.new),
    path('products/create', views.create),
    path('category/<int:category_id>', views.show_category),
    path('buy', views.buy),
    path('reset', views.reset),
]