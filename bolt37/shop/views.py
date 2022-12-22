from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from .models import Category

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']


def index(request):
    posts = Category.objects.all()
    return render(request, 'shop/index.html', {'posts': posts, 'menu': menu, 'title': 'Main page'})


def about(request):
    return render(request, 'shop/about.html', {'title': 'About'})


def categories(request, cat):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1> Articles by category <h1><p>{cat}<p>')


def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    elif int(year) < 2000:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
