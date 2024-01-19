from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count

from apps.supplier.models import Supplier
from apps.order.models import Order
from apps.product.models import Product, Category, Variant
from apps.payment.models import Payee, Payment, Income, Source


# Create your views here.
@login_required
def dashboard(request):
    order = Order.objects.aggregate(
        total_tax=Sum('total_taxes'),
        total_amount=Sum('total_amount'),
        total_more=Sum('additional_costs'),
        total_orders = Count('id')
                )
    total_payment_amount = Payment.objects.filter(
        paid=True).aggregate(
            total_payment_amount=Sum(F('amount')))['total_payment_amount']
    total_income_amount = Income.objects.aggregate(
        total_income=Sum('amount'))['total_income']  
    context = {
            'total_orders': order['total_orders'],
            'total_payments': Payment.objects.count(),
            'total_payees': Payee.objects.count(),
            'total_income': Income.objects.count(),
            'total_sources': Source.objects.count(),
            'total_variants': Variant.objects.count(),
            'total_categories': Category.objects.count(),
            'total_products': Product.objects.count(),
            'total_suppliers': Supplier.objects.count(),
            'total_tax': '{:.2f} €'.format(order['total_tax']) if order['total_tax'] is not None else '0.00 €',
            'total_amount': '{:.2f} €'.format(order['total_amount']) if order['total_amount'] is not None else '0.00 €',
            'total_more': '{:.2f} €'.format(order['total_more']) if order['total_more'] is not None else '0.00 €',
            'total_payment_amount': '{:.2f} €'.format(total_payment_amount) if total_payment_amount is not None else '0.00 €',
            'total_income_amount': '{:.2f} €'.format(total_income_amount) if total_income_amount is not None else '0.00 €',         
        }
    return render(request, 'dash/index.html', context)
