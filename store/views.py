from django.shortcuts import render, redirect
from .forms import *
from .models import *


def index(request):
    context = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'store/index.html', context)


def show_category(request, category_id):
    try:
        target_category = Category.objects.get(id=category_id)
    except KeyError:
        return redirect('/')
    context = {
        'target_category': target_category,
        'products': target_category.products.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'store/category.html', context)


def show_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except KeyError:
        return redirect('/')
    context = {
        'product': product,
        'prices': product.generate_prices(),
    }
    return render(request, 'store/product_page.html', context)


def show_cart(request):
    return render(request, 'store/cart.html')


def new(request):
    context = {
        'form': ProductForm(),
    }
    return render(request, 'store/new.html', context)


def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('success')
            product_category = Category.objects.get_or_create(name=form.cleaned_data['category'])[0]
            Product.objects.create(name=form.cleaned_data['name'],
                                   desc=form.cleaned_data['desc'],
                                   category=product_category,
                                   price=form.cleaned_data['price'],
                                   thumbnail=request.FILES['file'])
            return redirect('/products/new')
    return redirect('/products/new')


def sort(request, sort_by):
    context = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
    }
    if sort_by == 'price':
        return render(request, 'store/sort_by_price.html', context)
    if sort_by == 'popular':
        return render(request, 'store/sort_by_popularity.html', context)

