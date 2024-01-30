from decimal import Decimal
from django.db.models import Sum, Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Payee, PayeeType, Payment, Source, Income
from .forms import (PaymentForm, PayeeForm, PayeeTypeForm,
                    PayeeUpdateForm, PaymentUpdateForm,
                    SourceForm, IncomeForm)


@login_required
def payment_statistics(request):
    payees = Payee.objects.all()
    payments = Payment.objects.all()
    income = Income.objects.all()
    payee_types = PayeeType.objects.all()

    num_sources = Source.objects.count()
    num_payees = payees.count()
    total_income = income.aggregate(total_income=Sum('amount'))['total_income'] or Decimal('0.00')
    total_payments = payments.aggregate(total_payments=Sum('amount'))['total_payments'] or Decimal('0.00')

     # Payee Statistics
    payee_statistics = payees.values('name').annotate(
        total_payments=Sum('payment__amount'),
        average_payment=Avg('payment__amount'),
        payment_frequency=Count('payment')
    )
    payee_type_statistics = payee_types.values('label').annotate(
        total_payments=Sum('payee__payment__amount'),
        average_payment=Avg('payee__payment__amount'),
        payment_frequency=Count('payee__payment')
    )
    income_statistics = income.values('source_id__source').annotate(
        average_income=Avg('amount'),
        total_income=Sum('amount'),
        income_frequency=Count('id')
    )
    # Payment Statistics
    largest_payments = payments.order_by('-amount')[:10]  #

    # Financial Health Metrics
    income_to_expense_ratio = total_income / total_payments if total_payments != 0 else None
    expense_to_income_ratio = total_payments / total_income if total_income != 0 else None

    context = {
        'num_sources': num_sources,
        'num_payees': num_payees,
        'total_income': total_income,
        'total_payments': total_payments,
        'payee_statistics': payee_statistics,
        'payee_type_statistics': payee_type_statistics,
        'income_statistics': income_statistics,
        'expense_to_income_ratio':expense_to_income_ratio,
        'largest_payments': largest_payments,
        'income_to_expense_ratio': income_to_expense_ratio,
    }

    return render(request, 'payment/statistics.html', context)
@login_required
def payment(request):
    context = {}
    objs = Payment.objects.all()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής προσθήκη Πληρωμής") 
            return redirect('payment:payment')           
    else:
        form = PaymentForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'payment/payment.html' , context)

@login_required
def update_payment(request, id):
    context = {}
    payment = get_object_or_404(Payment, id=id)
    if request.method == 'POST':
        form = PaymentUpdateForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()            
            return redirect('payment:payment')
    else:
        form = PaymentUpdateForm(instance=payment)
    context['form'] = form
    return render(request, 'payment/update.html' , context)

@login_required
def delete_payment(request, id):
    obj = get_object_or_404(Payment, id = id)
    obj.delete()
    return redirect('payment:payment')

@login_required
def payee_label(request):
    context = {}
    objs = PayeeType.objects.all()

    if request.method == 'POST':
        form = PayeeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής προσθήκη Κατηγορίας")
    else:
        form = PayeeTypeForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'payment/payee_label.html' , context)

@login_required
def delete_payee_label(request, id):
    obj = get_object_or_404(PayeeType, id = id)
    obj.delete()
    return redirect('payment:payee-label')

@login_required
def payee(request):
    context = {}
    objs = Payee.objects.all()

    if request.method == 'POST':
        form = PayeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Προσθήκη Παραλήπτη")
    else:
        form = PayeeForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'payment/payee.html' , context)

@login_required
def delete_payee(request, id):
    obj = get_object_or_404(Payee, id = id)
    obj.delete()
    messages.error(request, f'Διαγραφηκε ο Παραλήπτης:{obj}')
    return redirect('payment:payee')

@login_required
def update_payee(request, payee_id):
    context = {}
    payee = get_object_or_404(Payee, id=payee_id)
    if request.method == 'POST':
        form = PayeeUpdateForm(request.POST, instance=payee)
        if form.is_valid():
            form.save()
            return redirect('payment:payee')
    else:
        form = PayeeUpdateForm(instance=payee)
    context['form'] = form
    return render(request, 'payment/payee_update.html' , context)


@login_required
def source(request):
    context = {}
    objs = Source.objects.all()

    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Δημιουργία Πηγής")
            return redirect ('payment-source')
    else:
        form = SourceForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'payment/source.html' , context)

@login_required
def delete_source(request, id):
    obj = get_object_or_404(Source, id = id)
    obj.delete()
    return redirect('payment:source')

@login_required
def income(request):
    context = {}
    objs = Income.objects.all()

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Επιτυχής Δημιουργία Εισοδήματος")
            return redirect('payment:income')
    else:
        form = IncomeForm()
    context['form'] = form
    context['objs'] = objs
    return render(request, 'payment/income.html' , context)

@login_required
def delete_income(request, id):
    obj = get_object_or_404(Income, id = id)
    obj.delete()
    return redirect('payment:income')