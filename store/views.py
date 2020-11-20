from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *


def index(request):
    sort_by = request.GET.get('s', 'price-asc')
    if sort_by == 'price-asc':
        all_products = Product.objects.all().order_by('price')
    elif sort_by == 'price-desc':
        all_products = Product.objects.all().order_by('-price')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 3)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'cat_name': 'All',
        's': sort_by,
        'products': products,
        'categories': Category.objects.all(),
    }
    if request.GET.get('show') == 'sort':
        return render(request, 'store/sort.html', context)
    return render(request, 'store/index.html', context)


def show_category(request, category_id):
    try:
        target_category = Category.objects.get(id=category_id)
    except KeyError:
        return redirect('/')
    sort_by = request.GET.get('s', 'price-asc')
    if sort_by == 'price-asc':
        products = target_category.products.all().order_by('price')
    if sort_by == 'price-desc':
        products = target_category.products.all().order_by('-price')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 3)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        's': sort_by,
        'cat_name': target_category.name,
        'products': products,
        'categories': Category.objects.all(),
    }
    if request.GET.get('show') == 'sort':
        return render(request, 'store/sort.html', context)
    return render(request, 'store/index.html', context)


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

