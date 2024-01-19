import re
from django import forms

from .models import Supplier, Shop, SupplierShop

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company', 'tin', 'phone', 'city', ]
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Επωνυμία'}),
            'tin': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '9 ψηφία',
                                            'max': 999999999}),           
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                              'max': 9999999999,
                                              'placeholder': 'π.χ 6906975208'}),
            'city': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Εδρα'}),
            
        }
class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company', 'tin', 'phone', 'city', 'summary']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Επωνυμία'}),
            'tin': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '9 ψηφία',
                                            'max': 999999999}),           
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                              'max': 9999999999,
                                              'placeholder': 'π.χ 6906975208'}),
            'city': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Εδρα'}),
            'summary': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Εισάγετε Σχόλια για τον Προμηθευτή...'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Check if the phone number is a 10-digit number
        if not re.match(r'^\d{10}$', str(phone)) and phone is not None:
            raise forms.ValidationError("Phone number must be a 10-digit number.")

        return phone
    
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_code',]
        widgets = {
            'shop_code': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Κωδικός Καταστήματος, π.χ Δ-30'}),}
          

class SupplierShopForm(forms.ModelForm):
    shop_id = forms.ModelChoiceField(
        queryset=Shop.objects.filter(assigned=False),  # Filter the queryset
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = SupplierShop
        fields = ['shop_id', 'supplier_id', ]
        widgets = {
            'supplier_id': forms.Select(attrs={'class': 'form-control',}),
        }

    