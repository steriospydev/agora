from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Variant, Product
from .forms import ProductForm, CategoryForm, VariantForm
from .charts import construct_product_charts

from apps.order.models import OrderItem

@login_required
def product(request):
    context = {
        'total_variants': Variant.objects.count(),
        'total_categories': Category.objects.count(),
        'total_products': Product.objects.count(),
    }
    objs = Product.objects.all().order_by('-category')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Δημιουργία Προιόντος")
    else:
        form = ProductForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'product/product.html' , context)

@login_required
def product_stats(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {}

    data = OrderItem.objects.filter(product=obj)
    if data:        
        context['data_summary'], context['price_track'] = construct_product_charts(data)  
    context['obj'] = obj
    return render(request, 'product/product_stats.html', context)


@login_required
def delete_product(request, id):
    obj = get_object_or_404(Product, id = id)
    obj.delete()
    messages.error(request, f'Διαγραφηκε το προιόν:{obj}')
    return redirect('product:product')

@login_required
def variant(request):
    context = {}
    objs = Variant.objects.all()

    if request.method == 'POST':
        form = VariantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής προσθήκη Ποικιλίας")
    else:
        form = VariantForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'product/variant.html' , context)

@login_required
def delete_variant(request, id):
    obj = get_object_or_404(Variant, id = id)
    obj.delete()
    return redirect('product:variant')

@login_required
def category(request):
    context = {}
    objs = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής προσθήκη Καταστήματος")
    else:
        form = CategoryForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'product/category.html' , context)

@login_required
def delete_category(request, id):
    obj = get_object_or_404(Category, id = id)
    obj.delete()
    return redirect('product:category')