from django.urls import include, path

from .views import (
    About,
    AddProduct,
    Contact,
    FilterProduct,
    LoginUser,
    LogoutUser,
    Products_by_Categories,
    RegisterUser,
    Search,
    ShopHome,
    ShowProduct,
)

product_patterns = [
    path('', Products_by_Categories.as_view(), name='categories'),
    path('filter/', FilterProduct.as_view(), name='filter_product'),
    path('<slug:product_slug>/', ShowProduct.as_view(), name='product_page'),
]

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('search/', Search.as_view(), name='search'),
    # path('filter/', FilterProduct.as_view(), name='filter_product'),
    path('<slug:cate>/', include(product_patterns)),
]
