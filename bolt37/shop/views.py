from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect


def index(request):
    return HttpResponse('Page of app shop')


def categories(request, cat):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1> Articles by category <h1><p>{cat}<p>')


def archive(request, year):
    if int(year) > 2020:
        raise Http404()
    elif int(year) < 2000:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
