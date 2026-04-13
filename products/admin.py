from django.contrib import admin
from .models import (
    Product, Attribute, AttributeValue,
    ProductVariant, VariantAttribute, ProductAttribute
)


class VariantAttributeInline(admin.TabularInline):
    model = VariantAttribute
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'stock']
    list_filter = ['product']
    inlines = [VariantAttributeInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured']


admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)