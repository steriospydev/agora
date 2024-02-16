import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


from config.utils import TimeStampedModel

class Supplier(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.CharField("Επωνυμία", max_length=120, unique=True)
    phone = models.CharField("Τηλέφωνο", max_length=10, blank=True, null=True,
                             validators=[
                                 RegexValidator(
                                     regex=r'^\d{10}$',
                                     message="Phone number must be entered as 10"
                                            " digits.No other punctuation required."
                                )])
    city = models.CharField("Εδρα",max_length=200, blank=True)
    tin = models.CharField("Α.Φ.Μ.",max_length=9,
                           validators=[
                                RegexValidator(
                                    regex=r"^[0-9]{9}$",
                                    message="Invalid Greek TIN number."
                                            " It must contain 9 digits.")],
                               unique=True) 
    summary = models.TextField("Περιγραφή", blank=True)
    
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['-created_at']
    
    def get_absolute_url(self):
        return reverse('supplier:supplier-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.company}'
    
    def delete(self):
        try:
            supplier_shop = SupplierShop.objects.get(supplier_id=self)
            shop = Shop.objects.get(shop_code=supplier_shop.shop_id)
            shop.assigned = False
            shop.save()            
        except SupplierShop.DoesNotExist:
            supplier_shop = None             
        super().delete()

class Shop(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    shop_code = models.CharField(max_length=30, unique=True)        
    assigned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['shop_code']

    def __str__(self) -> str:
         return f'{self.shop_code}'
  
    
class SupplierShop(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    shop_id = models.OneToOneField('Shop', on_delete=models.CASCADE)
    supplier_id = models.OneToOneField('Supplier', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.supplier_id.company} - {self.shop_id.shop_code}'

    class Meta:
        unique_together = ['shop_id', 'supplier_id']

    def save(self):
        self.shop_id.assigned = True
        self.shop_id.save()
        return super().save()
    
    def delete(self):
        self.shop_id.assigned = False
        self.shop_id.save()
        return super().delete()