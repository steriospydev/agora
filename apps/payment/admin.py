from django.contrib import admin
from .models import PayeeType, Payee, Payment
# Register your models here.

admin.site.register(PayeeType)
admin.site.register(Payee)
admin.site.register(Payment)


