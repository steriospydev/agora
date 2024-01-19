from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Category, Variant, Product

class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["category_name", ]

class VariantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["variant_name", ]

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["product_name", "quality", "category", "variant" ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Product, ProductAdmin)