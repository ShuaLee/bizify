from django.contrib import admin
from django.db import models
from .models import Inventory, Item
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'item_count')
    list_filter = ('company',)
    search_fields = ('name',)
    inlines = [ItemInline]
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget}
    }

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'quantity')
    list_filter = ('inventory__company', 'inventory')
    search_fields = ('name', 'description')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
