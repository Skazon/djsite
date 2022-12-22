from django.urls import path, re_path

from .views import about, archive, categories, index

urlpatterns = [
    path('', index, name='home'),  # http://127.0.0.1:8000/
    path('about/', about, name='about'),  # http://127.0.0.1:8000/about/
    path('cats/<slug:cat>/', categories),  # http://127.0.0.1:8000/cats/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
