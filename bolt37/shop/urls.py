from django.urls import include, path

from .views import About, AddProduct, Contact, Login, Products_by_Categories, ShopHome, ShowProduct

product_patterns = [
    path('', Products_by_Categories.as_view(), name='categories'),
    path('<slug:product_slug>/', ShowProduct.as_view(), name='product_page'),
]

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('login/', Login.as_view(), name='login'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('<slug:cate>/', include(product_patterns)),
]
