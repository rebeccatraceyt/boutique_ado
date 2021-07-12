from django.contrib import admin
from .models import Product, Category

# Extend built-in model admin class to view on /admin/.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)
    # sort products by 'sku'
    # reverse it using -'sku'
    # comma needed for tuple
    


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
