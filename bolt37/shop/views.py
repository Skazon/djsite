from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from shop.forms import AddPostForm
from shop.models import Category, Product

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Контакты', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница',
    }
    return render(request, 'shop/base.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте',
    }
    return render(request, 'shop/about.html', context=context)


def contact(request):
    context = {
        'menu': menu,
        'title': 'Контакты',
    }
    return render(request, 'shop/base.html', context=context)


def login(request):
    context = {
        'menu': menu,
        'title': 'Вход',
    }
    return render(request, 'shop/base.html', context=context)


def categories(request, cate):
    if request.GET:
        print(request.GET)

    selected_category = Category.objects.get(slug=cate)
    products = selected_category.products.all()

    context = {
        'menu': menu,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'shop/index.html', context=context)


def show_product_page(request, cate, product_slug):
    selected_product = get_object_or_404(Product, slug=product_slug)

    context = {
        'menu': menu,
        'selected_category': selected_product.category,
        'selected_product': selected_product,
    }
    return render(request, 'shop/product_page.html', context=context)


def add_product(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Product.objects.create(**form.cleaned_data)
                return redirect('home')
            except IntegrityError:
                form.add_error(None, 'Ошибка добавления товара')
    else:
        form = AddPostForm()

    context = {
        'menu': menu,
        'form': form,
    }
    return render(request, 'shop/add_page.html', context=context)


def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    elif int(year) < 2000:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
