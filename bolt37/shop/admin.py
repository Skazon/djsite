from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'slug', 'price', 'stock', 'available', 'get_image')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_editable = ('available', )
    list_filter = ('category', 'available')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('category', 'name', 'slug', 'image', 'get_image', 'description', 'price', 'stock', 'available')
    readonly_fields = ('get_image',)
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=60>')

    get_image.short_description = 'Изображение'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'moder')
    list_display_links = ('id', )
    search_fields = ('product', )
    list_editable = ('moder', )
    list_filter = ('product', 'user')
    fields = ('user', 'product', 'image', 'get_image', 'advantages', 'drawbacks', 'text', 'rating', 'moder')
    readonly_fields = ('user', 'get_image')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=60>')

    get_image.short_description = 'Изображение'
