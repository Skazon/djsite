from django import template

from shop.models import Category


register = template.Library()


@register.simple_tag(name='get_menu')
def get_menu():
    menu = [
        {'title': 'Главная', 'url_name': 'home'},
        {'title': 'Добавить', 'url_name': 'add_product'},
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
    ]
    return menu


@register.inclusion_tag('shop/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
