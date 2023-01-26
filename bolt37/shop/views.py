from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from shop.forms import AddPostForm, RegisterUserForm
from shop.models import Category, Product


class BaseTemplateView(TemplateView):
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ShopHome(BaseTemplateView):
    template_name = 'shop/base.html'
    title = 'Главная страница'


class About(BaseTemplateView):
    template_name = 'shop/about.html'
    title = 'О сайте'


class Contact(BaseTemplateView):
    template_name = 'shop/base.html'
    title = 'Контакты'


class Login(BaseTemplateView):
    template_name = 'shop/base.html'
    title = 'Вход'


class Products_by_Categories(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = Category.objects.get(slug=self.kwargs['cate'])
        context['title'] = selected_category.name
        context['selected_category'] = selected_category
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['cate'])


class ShowProduct(DetailView):
    model = Product
    template_name = 'shop/product_page.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'selected_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context['selected_category'] = self.object.category
        return context


class AddProduct(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'shop/add_page.html'
    success_url = reverse_lazy('home')  # Если не указать, то перейдет на созданную страницу,
    # если определен get_absolute_url()
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление пользовательского товара'
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
