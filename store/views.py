from django.shortcuts import render, redirect


def index(request):
    return render(request, 'store/index.html')


def show_product(request, product_id):
    return render(request, 'store/product_page.html')


def show_cart(request):
    return render(request, 'store/cart.html')

