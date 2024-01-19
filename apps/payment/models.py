import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone

from config.utils import TimeStampedModel


class PayeeType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.label}'

class Payee(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.ForeignKey(PayeeType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    summary = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}-{self.label}'
    
    def get_absolute_url(self):
        return reverse('payment:payee-update', args=[str(self.id)])
    
    class Meta:
        unique_together = ['label', 'name']

class Payment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payee = models.ForeignKey(Payee, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    summary = models.CharField(max_length=200, blank=True, null=True)
    payment_day = models.DateTimeField(blank=True, null=True, default=timezone.now)
    paid = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('payment:payment-update', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.payee} - {self.created_at.strftime("%b %d %Y")}'
    
    class Meta:
        ordering = ['paid', '-payment_day']


class Source(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=40, unique=True)
    summary = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.source}'

class Income(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_id = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    summary = models.CharField(max_length=200, blank=True, null=True)
    income_date =models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self) -> str:
        return f'{self.source_id} - {self.amount}'