from django.urls import path, re_path

from .views import about, archive, categories, contact, index, login

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('categories/<slug:cate>/', categories, name='categories'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
