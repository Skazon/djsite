from django import template

from shop.models import Category


register = template.Library()


@register.simple_tag(name='get_cats')
def get_categories(custom_filter=None):
    if not custom_filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=custom_filter)


@register.inclusion_tag('shop/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
