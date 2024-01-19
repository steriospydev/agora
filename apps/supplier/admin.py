from django.contrib import admin
from .models import Shop, Supplier, SupplierShop
# Register your models here.

admin.site.register(Shop)
admin.site.register(Supplier)
admin.site.register(SupplierShop)