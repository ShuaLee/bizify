from rest_framework import serializers
from .models import Inventory, Item, Attribute, ItemAttribute


class ItemAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAttribute
        fields = ['id', 'attribute', 'value']

    def validate(self, data):
        attribute = data.get('attribute')
        value = data.get('value')
        item = self.context.get('item') or (
            self.instance and self.instance.item)

        # Ensure attribute belongs to the item's inventory
        if item and attribute.inventory != item.inventory:
            raise serializers.ValidationError(
                f"Attribute '{attribute.name}' does not belong to inventory '{item.inventory.name}'."
            )

        # Validate value against field_type
        field_type = attribute.field_type
        if field_type == 'text' and not isinstance(value, str):
            raise serializers.ValidationError("Value must be a text string.")
        elif field_type == 'number':
            try:
                float(value)
            except (ValueError, TypeError):
                raise serializers.ValidationError("Value must be a number.")
        elif field_type == 'bool':
            if value.lower() not in ('true', 'false', '1', '0'):
                raise serializers.ValidationError(
                    "Value must be a boolean ('true' or 'false').")
        elif field_type == 'url' and not isinstance(value, str):
            raise serializers.ValidationError("Value must be a URL string.")

        # Check allow_multiple (only one value unless allowed)
        if not attribute.allow_multiple and ItemAttribute.objects.filter(item=item, attribute=attribute).exists() and not self.instance:
            raise serializers.ValidationError(
                f"Attribute '{attribute.name}' does not allow multiple values; an entry already exists."
            )

        return data


class ItemSerializer(serializers.ModelSerializer):
    attributes = ItemAttributeSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = ['id', 'inventory', 'name', 'description',
                  'quantity', 'attributes', 'created_at', 'updated_at']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        item = Item.objects.create(**validated_data)
        for attr_data in attributes_data:
            ItemAttributeSerializer(context={'item': item}).create(attr_data)
        return item

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        # Update or create ItemAttributes
        existing_attrs = {
            attr.attribute_id: attr for attr in instance.attributes.all()}
        for attr_data in attributes_data:
            attr_id = attr_data['attribute'].id
            if attr_id in existing_attrs:
                serializer = ItemAttributeSerializer(
                    existing_attrs[attr_id],
                    data=attr_data,
                    context={'item': instance}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                del existing_attrs[attr_id]
            else:
                ItemAttributeSerializer(
                    context={'item': instance}).create(attr_data)

        # Delete any remaining attributes not in the update
        for attr in existing_attrs.values():
            attr.delete()

        return instance


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'inventory', 'name', 'field_type', 'allow_multiple']

    def validate(self, data):
        inventory = data.get(
            'inventory', self.instance.inventory if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)
        if inventory and name and Attribute.objects.filter(inventory=inventory, name=name).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(
                f"Attribute '{name}' already exists for this inventory.")
        return data


class InventorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'company', 'name', 'attributes', 'items', 'created_at']
