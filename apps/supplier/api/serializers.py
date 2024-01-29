from rest_framework import serializers
from ..models import Supplier, Shop, SupplierShop


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company', 'phone', 'city', 'tin']