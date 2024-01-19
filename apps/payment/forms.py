from django import forms

from .models import Payment, Payee, PayeeType, Income, Source


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payee', 'amount', 'payment_day', 'paid']
        widgets = {
            'payee': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'Επωνυμία'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                                'min':0}),
            'payment_day': DateInput(attrs={'class': 'form-control','data-date-format': 'dd/mm/yyyy'}),  
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input p-2 bg-primary'}),                                                             
        }
class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payee', 'amount', 'payment_day', 'paid', 'summary']
        widgets = {
            'payee': forms.Select(attrs={'class': 'form-control',
                                              'placeholder': 'Επωνυμία'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                                'min':0}),
            'summary': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Προσθήκη Περιγραφής...'}),
            'payment_day':DateInput(attrs={'class': 'form-control','data-date-format': 'dd/mm/yyyy'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input p-2 bg-primary'}),
        }       

class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields = ['name', 'label',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Όνομα Παραλήπτη'}),
            'label': forms.Select(attrs={'class': 'form-control'}),  
            # 'active': forms.CheckboxInput(attrs={'class': ''}),     
            # 'summary': forms.Textarea(attrs={'class': 'form-control',
            #                                   'placeholder': 'Προσθήκη Περιγραφής...'}),
    
        }

class PayeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields = ['name', 'label','active', 'summary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Όνομα Παραλήπτη'}),
            'label': forms.Select(attrs={'class': 'form-control'}),  
            'active': forms.CheckboxInput(attrs={'class': ''}),     
            'summary': forms.Textarea(attrs={'class': 'form-control',
                                              'placeholder': 'Προσθήκη Περιγραφής...'}),
    
        }

class PayeeTypeForm(forms.ModelForm):
    class Meta:
        model = PayeeType
        fields = ['label',]
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Όνομα Κατηγορίας Πληρωμών'}),
           
        }

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['source', 'summary']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Πηγή Εισοδήματος'}),
            'summary': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Προσθήκη Περιγραφής...'}),\
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source_id', 'amount', 'income_date', 'summary']
        widgets = {
            'source_id': forms.Select(attrs={'class': 'form-control',
                                          'placeholder': 'Πηγή Εισοδήματος'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                              'min': 0}),
            'income_date': DateInput(attrs={'class': 'form-control',
                                            'data-date-format': 'dd/mm/yyyy'}),  
            'summary': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Περιγραφή'}),
        }