from django.shortcuts import render, redirect
from .forms import *
from .models import *


def index(request):
    return render(request, 'store/index.html')


def show_product(request, product_id):
    return render(request, 'store/product_page.html')


def show_cart(request):
    return render(request, 'store/cart.html')


def new(request):
    context = {'form': ProductForm()}
    return render(request, 'store/new.html', context)


def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print('success')
            product_category = Category.objects.get_or_create(name=form.cleaned_data['category'])[0]
            Product.objects.create(name=form.cleaned_data['name'],
                                   desc=form.cleaned_data['desc'],
                                   category=product_category,
                                   price=form.cleaned_data['price'])
            return redirect('/products/new')

    return redirect('/products/new')


def upload(request, product_id):
    pass
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         return
