from django import forms

from .models import Order,OrderItem




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'total_costs', 'total_taxes','additional_costs',
                    'total_amount']
        widgets = {
            'total_costs': forms.TextInput(attrs={'class': 'form-control',
                                            'disabled': 'disabled',
                                            'placeholder':'0.00'}),           
            'total_taxes': forms.TextInput(attrs={'class': 'form-control',            
                                              'disabled': 'disabled',
                                            'placeholder':'0.00'}),
            'additional_costs': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder':'0.00'}),            
            'total_amount': forms.TextInput(attrs={'class': 'form-control',
                                                     'disabled': 'disabled',
                                            'placeholder':'0.00'}),
        }

        
class OrderItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        order_id = kwargs.pop('order_id', None)  # Pop the order_id from kwargs
        super(OrderItemForm, self).__init__(*args, **kwargs)

        if order_id is not None:
            self.fields['order'].initial = order_id  # Set the initial value of the 'order' field

    class Meta:
        model = OrderItem
        fields = [ 'product', 'order','shop', 
                   'source',
                   'quantity', 'unit_price','tax_rate',
                   
                   ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),  
            'order': forms.Select(attrs={'class': 'form-control',}), 
            'shop': forms.Select(attrs={'class': 'form-control'}), 

            'source': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Προέλευση'}), 
            'quantity': forms.NumberInput(attrs={'class': 'form-control','min':0}),  
            'unit_price': forms.NumberInput(attrs={'class': 'form-control','min':0}), 
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control',
                                                 'max':100,'min':0}),            
        
        }