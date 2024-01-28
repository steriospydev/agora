from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .charts import construct_supplier_charts
from .models import Supplier, Shop, SupplierShop
from .forms import (SupplierForm, SupplierUpdateForm,
                    ShopForm, SupplierShopForm)

from apps.order.models import OrderItem

class SupplierView(LoginRequiredMixin, View):
    template_name = 'supplier/supplier.html'
    login_url = 'your_login_url' 

    def get_context_data(self, form):
        objs = Supplier.objects.all()
        context = {
            'objs': objs,
            'form': form,
            'supplier_count': objs.count(),
            'shop_count': Shop.objects.count()
        }
        return context

    def get(self, request, *args, **kwargs):
        form = SupplierForm()
        return render(request, self.template_name, self.get_context_data(form))

    def post(self, request, *args, **kwargs):
        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Προσθήκη Προμηθευτή")
            return redirect("supplier:supplier-list")

        return render(request, self.template_name, self.get_context_data(form))
    
# List objects
@login_required
def supplier(request):
    objs = Supplier.objects.all()

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Προσθήκη Προμηθευτή")
            return redirect("supplier:supplier-list")
    else:
        form = SupplierForm()

    context = {
        'objs': objs,
        'form': form,
        'supplier_count': objs.count(),
        'shop_count': Shop.objects.count()
    }
    return render(request, 'supplier/supplier.html', context)

@login_required
def shop(request):
    context = {}
    objs = Shop.objects.all()
    connected_objs = SupplierShop.objects.all()
    for obj in objs:
        connected_obj = connected_objs.filter(shop_id=obj.id).first()
        if connected_obj:
            obj.supplier_id = connected_obj.supplier_id
        else:
            obj.supplier_id = "Not connected"

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής προσθήκη Καταστήματος")
    else:
        form = ShopForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'supplier/shop.html' , context)

# Create/Update objects
@login_required
def supplier_update(request, id):
    context ={} 
    obj = get_object_or_404(Supplier, id = id)
    form = SupplierUpdateForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect(obj.get_absolute_url())
    context["form"] = form
    return render(request, "supplier/update.html", context)

@login_required
def supplier_detail(request, id):
    obj = get_object_or_404(Supplier, id=id)    
    context ={}

    if request.method == 'POST':        
        obj.delete()
        return redirect('supplier:supplier-list')   
    
    try:        
        shop = SupplierShop.objects.get(supplier_id=id)
        orders = OrderItem.objects.filter(shop=shop.shop_id) 
        if orders:
            order_summary = orders.values('product__product_name').annotate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('amount')
            )
            context['q_img'], context['a_img'] = construct_supplier_charts(order_summary)  
        context['shop'] = shop
    except SupplierShop.DoesNotExist:
        shop = None      

    context['obj'] = obj
    return render(request, 'supplier/detail.html', context)

@login_required
def connect_supplier_shop(request):  
    context = {}
    if request.method == 'POST':
        form = SupplierShopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Συνδεση Προμηθευτή-Μαγαζιού")
            return redirect('supplier:shop')
    else:
        form = SupplierShopForm()
    context['form'] = form
    return render(request, "supplier/create_connection.html", context)   

# Delete objects
@login_required
def supplier_shop_delete(request, shop_id):
    shop = get_object_or_404(SupplierShop, shop_id=shop_id)
    if request.method == 'POST':        
        shop.delete()
        messages.error(request, f"Επιτυχης Αποσυνδεση {shop}")
    return redirect('supplier:shop') 


