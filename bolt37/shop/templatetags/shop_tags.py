from django import template
from django.core.cache import cache

from shop.models import Category


register = template.Library()


@register.simple_tag(name='get_menu')
def get_menu():
    menu = [
        {'title': 'Главная', 'url_name': 'home'},
        {'title': 'Добавить', 'url_name': 'add_product'},
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contact'},
    ]
    return menu


@register.inclusion_tag('shop/list_categories.html')
def show_categories(cat_selected=0):
    cats = cache.get('cats')
    if cats is None:
        cats = Category.objects.all()
        cache.set('cats', cats, 60 * 60)
    return {'cats': cats, 'cat_selected': cat_selected}
