from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import Category, Variant, Product
from .forms import ProductForm, CategoryForm, VariantForm
from .charts import construct_product_charts

from apps.order.models import OrderItem


class BaseListView(LoginRequiredMixin, ListView):
    template_name = ''
    context_object_name = 'objs'
    paginate_by = 8
    form_class = None
    success_message = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class() if self.form_class else None
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if self.success_message:
                messages.success(request, self.success_message)
        return self.get(request, *args, **kwargs)

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

@login_required
def delete_product(request, id):
    obj = get_object_or_404(Product, id = id)
    obj.delete()
    messages.error(request, f'Διαγραφηκε το προιόν:{obj}')
    return redirect('product:product')

@login_required
def delete_category(request, id):
    obj = get_object_or_404(Category, id = id)
    obj.delete()
    return redirect('product:category')

@login_required
def delete_variant(request, id):
    obj = get_object_or_404(Variant, id = id)
    obj.delete()
    return redirect('product:variant')

@login_required
def product_stats(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {}

    data = OrderItem.objects.filter(product=obj)
    if data:        
        context['data_summary'], context['price_track'] = construct_product_charts(data)  
    context['obj'] = obj
    return render(request, 'product/product_stats.html', context)
