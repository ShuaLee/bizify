from rest_framework import serializers
from .models import Inventory, Item, ItemDetail


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDetail
        fields = ['key', 'value']


class ItemSerializer(serializers.ModelSerializer):
    details = ItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'inventory', 'name', 'description',
                  'quantity', 'details', 'created_at', 'updated_at']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'company', 'name', 'created_at']
