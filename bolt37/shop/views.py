from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from .models import Category

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Контакты', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]
product_categories = Category.objects.all()
context = {
        'categories_view': product_categories,
        'menu': menu,
        'title': 'Главная страница',
    }


def index(request):
    context['title'] = 'Главная страница'
    return render(request, 'shop/base.html', context=context)


def about(request):
    context['title'] = 'О сайте'
    return render(request, 'shop/about.html', context=context)


def contact(request):
    context['title'] = 'Контакты'
    return render(request, 'shop/base.html', context=context)


def login(request):
    context['title'] = 'Вход'
    return render(request, 'shop/base.html', context=context)


def categories(request, cate):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1> Articles by category <h1><p>{cate}<p>')


def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    elif int(year) < 2000:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
