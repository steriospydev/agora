from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem

@login_required
def order(request):
    context = {}
    objs = Order.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Δημιουργία Παραγγελιας")
    else:
        form = OrderForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'order/order.html' , context)

@login_required
def delete_order(request, id):
    obj = get_object_or_404(Order, id = id)
    message = f'{obj.formatted_created_at} - {obj.id} '
    obj.delete()
    messages.error(request, f'Διαγραφηκε η παραγγελία:{message}')
    return redirect('order:order-list')

@login_required
def detail_order(request, id):
    obj = Order.objects.get(id=id)
    objs = OrderItem.objects.filter(order_id=obj)
    date = obj.created_at.strftime('%Y-%m-%d %H:%M')
    context = {
        'page_title': obj.id,
        'date': date,
        'obj': obj,
        'objs': objs
    }
    return render(request, 'order/detail.html', context)

@login_required
def update_order(request, order_id):
    context = {}
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order:order-detail',id=order_id)
    else:
        form = OrderForm(instance=order)
    context['form'] = form
    return render(request, 'order/update.html' , context)

@login_required
def add_product(request, order_id):
    context = {}

    if request.method == 'POST':
        form = OrderItemForm(request.POST, order_id=order_id)
        
        if form.is_valid():
            print(f'Quantity: {type(form.cleaned_data["quantity"])}, Unit Price: {type(form.cleaned_data["unit_price"])}, Tax Rate: {type(form.cleaned_data["tax_rate"])}')
            form.save()
            messages.success(request, "Επιτυχής Εισαγωγή Προιόντος")
            return redirect('order:order-detail',id=order_id)
    else:
        form = OrderItemForm(order_id=order_id)
    context['form'] = form
    return render(request, 'order/add_product.html' , context)

@login_required
def update_order_item(request, item_id):
    context = {}
    item = get_object_or_404(OrderItem, id=item_id)
    order = get_object_or_404(Order, id=item.order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('order:order-detail',id=order.id)
    else:
        form = OrderItemForm(instance=item)
    context['form'] = form
    return render(request, 'order/update_product.html' , context)

@login_required
def remove_product(request, order_id, id):
    obj = get_object_or_404(OrderItem, id = id)
    obj.delete()
    return redirect('order:order-detail', id=order_id) 
