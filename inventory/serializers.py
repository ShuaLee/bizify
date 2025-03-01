from rest_framework import serializers
from .models import Inventory, Item, ItemDetail, InventorySetting


class ItemDetailSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='setting.key', read_only=True)
    type = serializers.CharField(source='setting.type', read_only=True)

    class Meta:
        model = ItemDetail
        fields = ['key', 'type', 'value']


class ItemSerializer(serializers.ModelSerializer):
    details = ItemDetailSerializer(many=True, read_only=True)

    def validate(self, data):
        inventory = data.get(
            'inventory', self.instance.inventory if self.instance else None)
        if not inventory:
            raise serializers.ValidationError("Inventory is required.")
        settings = {s.key: s.allow_multiple for s in inventory.settings.all()}
        details = self.initial_data.get('details', []
                                        )
        for detail in details:
            key = detail.get('key')
            if key not in settings:
                raise serializers.ValidationError(
                    f"Key '{key}' not defined in inventory settings.")
            value = detail.get('value')
            if not settings[key] and isinstance(value, list):
                raise serializers.ValidationError(
                    f"key '{key}' does not allow multiple values.")
        return data

    class Meta:
        model = Item
        fields = ['id', 'inventory', 'name', 'description',
                  'quantity', 'details', 'created_at', 'updated_at']

    class Meta:
        model = Item
        fields = ['id', 'inventory', 'name', 'description',
                  'quantity', 'details', 'created_at', 'updated_at']


class InventorySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventorySetting
        fields = ['id', 'key', 'type', 'allow_multiple']


class InventorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    settings = InventorySettingSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'company', 'name', 'items', 'settings', 'created_at']
