from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


# Displays a page showing all products.
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
        'session': request.session,
        'cat_name': 'All',
        's': sort_by,
        'products': products,
        'categories': Category.objects.all(),
    }
    if request.GET.get('show') == 'sort':
        return render(request, 'store/sort.html', context)
    return render(request, 'store/index.html', context)


# Displays a page showing products in a specific category.
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
        'session': request.session,
        's': sort_by,
        'cat_name': target_category.name,
        'products': products,
        'categories': Category.objects.all(),
    }
    if request.GET.get('show') == 'sort':
        return render(request, 'store/sort.html', context)
    return render(request, 'store/index.html', context)


# Displays a page showing product details.
def show_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except KeyError:
        return redirect('/')
    similar = product.category.products.exclude(id=product_id)
    similar = similar.order_by('?')[:3]
    context = {
        'session': request.session,
        'similar': similar,
        'product': product,
        'prices': product.generate_prices(),
    }
    return render(request, 'store/product_page.html', context)


# Displays a page showing the contents of the cart and a form for shipping
# and billing information.
def show_cart(request):
    print(request.session['cart'])
    cart_items = {}
    cart_total = 0
    try:
        for product_id, quantity in request.session['cart'].items():
            product = Product.objects.get(id=product_id)
            item = {
                'product_id': product_id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': quantity * product.price,
            }
            cart_total += quantity * product.price
            cart_items[product_id] = item
    except KeyError:
        cart_total = '0.00'
    context = {
        'cart_total': cart_total,
        'cart_items': cart_items,
        'products': Product.objects.all(),
        'session': request.session,
    }
    return render(request, 'store/cart.html', context)


# Displays a page for adding new products to the site.
@login_required(login_url='/')
def new(request):
    context = {
        'form': ProductForm(),
    }
    return render(request, 'store/new.html', context)


# Creates a new product for the site.
@login_required(login_url='/')
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('success')
            product_category = Category.objects.get_or_create(
                name=form.cleaned_data['category'])[0]
            new_product = Product.objects.create(
                name=form.cleaned_data['name'],
                desc=form.cleaned_data['desc'],
                category=product_category,
                price=form.cleaned_data['price'],
                thumbnail=request.FILES['file'])
            return redirect('/products/' + str(new_product.id))
    return redirect('/products/new')


# Increases the product's quantity in the cart by the selected amount.
def buy(request):
    if request.POST:
        quantity = int(request.POST['quantity'])
        product_id = request.POST['product_id']
        print(request.POST)
        try:
            request.session['item_count'] += quantity
        except KeyError:
            request.session['item_count'] = quantity
        if request.session.get('cart'):
            request.session['cart'][product_id] = request.session['cart'].get(
                product_id, 0) + quantity
        else:
            request.session['cart'] = {product_id: quantity}
        return render(request, 'store/update_cart.html',
                      {'session': request.session})
    return redirect('/')


# Clears the client's session.
def reset(request):
    request.session.flush()
    return redirect('/')


# Changes the quantity of a product in the cart or deletes a product from the
# cart.
def update_cart(request):
    if request.method == 'POST':
        cart = request.session['cart']
        product_id = request.POST['product_id']
        if request.POST['submit_type'] == 'update':
            cart[product_id] = int(request.POST['quantity'])
        else:
            del cart[product_id]
        item_count = 0
        for quantity in cart.values():
            item_count += quantity
        request.session['item_count'] = item_count
        request.session.modified = True
    return redirect('/cart')
