from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from config.utils import BaseListView, BaseDeleteView
from .models import Category, Variant, Product
from .forms import ProductForm, CategoryForm, VariantForm
from .charts import construct_product_charts

from apps.order.models import OrderItem

class ProductListView(BaseListView):
    model = Product
    template_name = 'product/product.html'
    form_class = ProductForm
    success_message = "Επιτυχής Δημιουργία Προιόντος"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional variables specific to ProductListView
        context['total_variants'] = Variant.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_products'] = Product.objects.count()
        return context
       
class CategoryListView(BaseListView):
    model = Category
    template_name = 'product/category.html'
    form_class = CategoryForm
    success_message = "Επιτυχής Δημιουργία Κατηγορίας"

class VariantListView(BaseListView):
    model = Variant
    template_name = 'product/variant.html'
    form_class = VariantForm
    success_message = "Επιτυχής Δημιουργία Ποικιλίας"


class ProductDeleteView(BaseDeleteView):
    model = Product
    redirect_url = 'product:product'
    success_message = 'Διαγραφηκε το προιόν: {}'

class CategoryDeleteView(BaseDeleteView):
    model = Category
    redirect_url = 'product:category'
    success_message = 'Διαγραφηκε η κατηγορια: {}'

class VariantDeleteView(BaseDeleteView):
    model = Variant
    redirect_url = 'product:variant'
    success_message = 'Διαγραφηκε η ποικιλία: {}'

@login_required
def product_stats(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {}

    data = OrderItem.objects.filter(product=obj)
    if data:        
        context['data_summary'], context['price_track'] = construct_product_charts(data)  
    context['obj'] = obj
    return render(request, 'product/product_stats.html', context)
