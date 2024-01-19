import uuid
from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_delete
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.urls import reverse

from config.utils import TimeStampedModel
from apps.product.models import Product
from apps.supplier.models import Shop

# Create your models here.
class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    total_costs = models.DecimalField(max_digits=8,decimal_places=2,
                                      default=00.00, blank=True)
    total_taxes = models.DecimalField(max_digits=8,decimal_places=2,
                                      default=00.00, blank=True)
    additional_costs = models.DecimalField(max_digits=8,decimal_places=2,
                                           default=00.00, blank=True)
    
    total_amount = models.DecimalField(max_digits=8,decimal_places=2,
                                       default=00.00, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{str(self.id)[:4]}'   
    
    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%b %d %Y")

    def calculate_total_taxes(self):
        self.total_taxes = sum([item.get_tax_total() for item in self.order_items.all()])
        return self.total_taxes

    def calculate_total_costs(self):
        self.subtotal = sum([item.get_amount() for item in self.order_items.all()])
        return self.subtotal

    def calculate_total_amount(self):
        self.total_amount = self.total_costs + self.total_taxes + self.additional_costs
        return self.total_amount
    
    def get_absolute_url(self):
        return reverse('order:order-detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_costs = self.calculate_total_costs()
        self.total_taxes = self.calculate_total_taxes()
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

class OrderItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_items')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items')
    source = models.CharField(max_length=30, blank=True, null=True)
    
    quantity = models.DecimalField(max_digits=8, decimal_places=2, 
                                   default=00.00, blank=True,
                                   validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=00.00, blank=True,validators=[MinValueValidator(0)])
    amount  = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=00.00, blank=True,validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField('Tax rate %', default=13.00,
                                   blank=True,
                                   max_digits=4, decimal_places=1,
                                   validators=[MinValueValidator(0)])
    taxes = models.DecimalField('Taxes', default=00.00,
                                blank=True,
                                max_digits=10, decimal_places=1,
                                validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                default=00.00, blank=True,validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f'{self.product.product_name}'
    
    def get_amount(self):
        return self.quantity * self.unit_price
    
    def get_tax_total(self):
        return self.get_amount() * (self.tax_rate /Decimal(100))

    def get_total(self):
        return self.get_amount() + self.get_tax_total()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.amount = self.get_amount()
        self.taxes = self.get_tax_total()
        self.total = self.get_total()
        super().save(*args, **kwargs)


@receiver(pre_save, sender=OrderItem)
@receiver(pre_delete, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_totals(sender, instance, **kwargs):
    # Get the associated order for the OrderItem
    order = instance.order

    # Update the totals for the order
    order.total_costs = order.calculate_total_costs()
    order.total_taxes = order.calculate_total_taxes()
    order.total_amount = order.calculate_total_amount()

    # Save the updated order
    order.save()
