from django import forms

from .models import Category


class AddPostForm(forms.Form):
    name = forms.CharField(max_length=255, label='Наименование')
    slug = forms.SlugField(max_length=255, label='URL')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Описание')
    price = forms.DecimalField(max_digits=10, decimal_places=2, label='Цена')
    available = forms.BooleanField(label='Доступно')
    stock = forms.IntegerField(label='На складе')
    # image = forms.ImageField()
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию'
    )
