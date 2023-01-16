from django.urls import include, path, re_path

from .views import about, archive, categories, contact, index, login, show_product_page

product_patterns = [
    path('', categories, name='categories'),
    path('<slug:product_slug>/', show_product_page, name='product_page'),
]

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('<slug:cate>/', include(product_patterns)),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
