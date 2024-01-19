from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('__str__', 'total_costs', 'total_taxes',
                    'additional_costs', 'total_amount')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('__str__','taxes', 'amount','total', 'unit_price', 
                    'quantity', 'tax_rate')
    list_editable = ('unit_price', 'quantity', 'tax_rate')