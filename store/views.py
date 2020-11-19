from django.shortcuts import render, redirect
from .forms import *
from .models import *


def index(request):
    return render(request, 'store/index.html')


def show_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except KeyError:
        return redirect('/')
    context = {
        'product': product,
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


# def upload(request, product_id):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             print('success')
#             instance = Product.objects.get(id=1)
#             instance.thumbnail = request.FILES['file']
#             instance.save()
#             return redirect('/products/new')
#     return redirect('/products/new')
