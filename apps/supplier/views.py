from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from config.utils import BaseListView, BaseUpdateView, BaseDeleteView
from .charts import construct_supplier_charts
from .models import Supplier, Shop, SupplierShop
from .forms import (SupplierForm, SupplierUpdateForm,
                    ShopForm, SupplierShopForm)

from apps.order.models import OrderItem

class SupplierListView(BaseListView):
    model = Supplier
    template_name = "supplier/supplier.html"
    form_class = SupplierForm
    success_message = "Επιτυχής Προσθήκη Προμηθευτή"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supplier_count"] = Supplier.objects.count()
        context["shop_count"] = Shop.objects.count()
        return context

class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    form_class = SupplierUpdateForm
    template_name = 'supplier/update.html'
    success_message = 'Επιτυχής ενημέρωση προμηθευτή'

class ShopListView(BaseListView):
    model = Shop
    template_name = 'supplier/shop.html'
    form_class = ShopForm
    success_message = 'Επιτυχής προσθήκη Καταστήματος'

    def get_queryset(self):
        objs = super().get_queryset()
        connected_objs = SupplierShop.objects.all()
        for obj in objs:
            connected_obj = connected_objs.filter(shop_id=obj.id).first()
            if connected_obj:
                obj.supplier_id = connected_obj.supplier_id
            else:
                obj.supplier_id = 'Not connected'
        return objs

class SupplierShopDeleteView(BaseDeleteView):
    model = SupplierShop
    redirect_url = 'supplier:shop'
    success_message = "Επιτυχης Αποσυνδεση {0}"
    
    def post(self, request, shop_id):
        obj = get_object_or_404(self.model, shop_id=shop_id)
        obj.delete()
        if self.success_message:
            messages.success(request, self.success_message.format(obj))
        return redirect(self.redirect_url)

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



