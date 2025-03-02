from django.contrib import admin
from django.db import models
from .models import Inventory, Item, Attribute, ItemAttribute
from django import forms


class ItemAttributeInline(admin.TabularInline):
    model = ItemAttribute
    extra = 1
    fields = ('attribute', 'value')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'attribute' and request._obj_:
            # Restrict attributes to the item's inventory
            kwargs['queryset'] = Attribute.objects.filter(
                inventory=request._obj_.inventory)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class InlineForm(formset.form):
            def clean_value(self):
                value = self.cleaned_data['value']
                attribute = self.cleaned_data.get('attribute')
                if attribute:
                    field_type = attribute.field_type
                    if field_type == 'text' and not isinstance(value, str):
                        raise forms.ValidationError(
                            "Value must be a text string.")
                    elif field_type == 'number':
                        try:
                            float(value)
                        except (ValueError, TypeError):
                            raise forms.ValidationError(
                                "Value must be a number.")
                    elif field_type == 'bool' and value.lower() not in ('true', 'false', '1', '0'):
                        raise forms.ValidationError(
                            "Value must be 'true' or 'false'.")
                    elif field_type == 'url' and not isinstance(value, str):
                        raise forms.ValidationError(
                            "Value must be a URL string.")
                return value
        formset.form = InlineForm
        return formset


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1
    fields = ('name', 'field_type', 'allow_multiple')


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    fields = ('name', 'description', 'quantity')
    inlines = [ItemAttributeInline]

    def get_form(self, request, obj=None, **kwargs):
        # Pass inventory to ItemAttributeInline
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'item_count', 'attribute_count')
    list_filter = ('company',)
    search_fields = ('name',)
    inlines = [AttributeInline, ItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

    def attribute_count(self, obj):
        return obj.attributes.count()
    attribute_count.short_description = 'Attributes'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'quantity')
    list_filter = ('inventory__company', 'inventory')
    search_fields = ('name', 'description')
    inlines = [ItemAttributeInline]

    def get_form(self, request, obj=None, **kwargs):
        # Pass item to ItemAttributeInline
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'field_type', 'allow_multiple')
    list_filter = ('inventory', 'field_type')
    search_fields = ('name',)


@admin.register(ItemAttribute)
class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = ('item', 'attribute', 'value')
    list_filter = ('attribute__inventory', 'attribute')
    search_fields = ('item__name', 'attribute__name', 'value')
