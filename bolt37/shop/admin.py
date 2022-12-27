from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', )
    search_fields = ('name', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'slug', 'price', 'stock', 'available')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_editable = ('available', )
    list_filter = ('category', 'available')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
