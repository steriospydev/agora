import uuid
from django.db import models
from django.urls import reverse
from config.utils import TimeStampedModel


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.category_name}'

class Variant(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant_name = models.CharField(max_length=100, unique=True)
    summary = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.variant_name}'
    
    class Meta:
        ordering = ['variant_name']

class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    QUALITIES = [("A", "A"),
                 ("B", "B"),
                 ("C", "C")]
    product_name = models.CharField(max_length=200)
    quality = models.CharField(max_length=1,
                               choices=QUALITIES, default=QUALITIES[0])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL,
                                default="empty", null=True)

    class Meta:
        unique_together = ['product_name', 'quality', "variant"]
        ordering = ['product_name']

    def __str__(self):
        return f'{self.product_name} {self.quality} {self.variant}'
    
    def get_absolute_url(self):
        return reverse('product:stats', args=[str(self.id)])