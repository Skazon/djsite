from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from shop.forms import AddPostForm, AddReview, LoginUserForm, RegisterUserForm
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


class ShopBaseListView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 10


class Prices:
    @classmethod
    def get_prices(cls, object_list: QuerySet):
        return object_list.values('price')


class Products_by_Categories(ShopBaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = Category.objects.get(slug=self.kwargs.get('cate'))
        context['title'] = selected_category.name
        context['selected_category'] = selected_category
        context['prices'] = Prices.get_prices(self.object_list)
        context['filter_url'] = self.get_filter_url()
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs.get('cate')).select_related('category')

    def get_filter_url(self):
        return reverse('filter_product', kwargs={'cate': self.kwargs.get('cate')})


class Search(ShopBaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))


class FilterProduct(Products_by_Categories):
    def get_queryset(self):
        filter_pattern = [float(value.replace(',', '.')) for value in self.request.GET.getlist('price')]
        return Product.objects.filter(price__in=filter_pattern).select_related('category')


class ShowProduct(FormMixin, DetailView):
    template_name = 'shop/product_page.html'
    context_object_name = 'selected_product'
    form_class = AddReview

    def get_object(self, queryset=None):
        return Product.objects.select_related('category').get(slug=self.kwargs.get('product_slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['selected_category'] = self.object.category
        context['reviews'] = self.object.reviews.all().select_related('user')
        context['use_form'] = True
        for review in context['reviews']:
            if self.request.user == review.user:
                context['use_form'] = False
        return context

    def get_success_url(self):
        return reverse_lazy(
            'product_page',
            kwargs={'cate': self.kwargs.get('cate'), 'product_slug': self.kwargs.get('product_slug')},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.product = self.object
                instance.user = request.user
                product_rating = self.object.rating
                product_number_of_ratings = len(self.object.reviews.all())
                self.object.rating = (product_rating * product_number_of_ratings + form.cleaned_data.get('rating')) / \
                                     (product_number_of_ratings + 1)
                self.object.save()
                form.save()
                return self.form_valid(form)
            except IntegrityError:
                form.add_error(None, 'Вы не можете создать еще один отзыв')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.cleaned_data['message'] = 'Успешно!'
        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    next_page = 'login'


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Page not found <h1>')
