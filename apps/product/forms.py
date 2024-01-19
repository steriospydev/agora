from django import forms

from .models import Product, Category, Variant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'quality', 'category', 'variant']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ονομασία Προιόντος'}),
            'quality': forms.Select(attrs={'class': 'form-control',}),    

            'category': forms.Select(attrs={'class': 'form-control',}),
            'variant': forms.Select(attrs={'class': 'form-control',}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ονομασία Κατηγορίας'}),
        }

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['variant_name', 'summary']
        widgets = {
            'variant_name': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ονομασία Ποικιλίας'}),
            'summary': forms.Textarea(attrs={'class': 'form-control',
                                              'placeholder': 'Περιγραφή Πικοιλίας'}),
        }