from rest_framework import serializers
from .models import Inventory, Item


class ItemSerializer(serializers.ModelSerializer):
    def validate_details(self, value):
        inventory = self.instance.inventory if self.instance else self.initial_data.get(
            'inventory')
        if isinstance(inventory, int):
            inventory = Inventory.objects.get(id=inventory)
        settings = inventory.settings
        for key in value:
            if key not in settings:
                raise serializers.ValidationError(
                    f"Key '{key}' not defined in inventory settings.")
            if not settings[key].get('allow_multiple', False) and isinstance(value[key], list):
                raise serializers.ValidationError(
                    f"Key '{key}' does not allow multiple values.")
        return value

    class Meta:
        model = Item
        fields = ['id', 'inventory', 'name', 'description',
                  'quantity', 'details', 'created_at', 'updated_at']


class InventorySerializer(serializers.ModelSerializer):
    VALUE_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('url', 'URL'),
        ('bool', 'Boolean'),
    )
    items = ItemSerializer(many=True, read_only=True)

    def validate_settings(self, value):
        for key, setting in value.items():
            if 'type' not in setting:
                raise serializers.ValidationError(
                    f"Setting '{key}' must specify a 'type'.")
            if setting['type'] not in dict(self.VALUE_TYPES):
                raise serializers.ValidationError(
                    f"Type '{setting['type']}' for '{key}' is not valid. Use: {', '.join(dict(self.VALUE_TYPES))}.")
            if 'allow_multiple' not in setting:
                raise serializers.ValidationError(
                    f"Setting '{key}' must specify 'allow_multiple'.")
        return value

    class Meta:
        model = Inventory
        fields = ['id', 'company', 'name', 'items', 'settings', 'created_at']
