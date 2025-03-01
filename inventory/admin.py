from django.contrib import admin
from .models import Inventory, ItemDetail, Item, InventorySetting

# Register your models here.


class ItemDetailInline(admin.TabularInline):
    model = ItemDetail
    extra = 1
    fields = ('setting', 'value')


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class InventorySettingInline(admin.TabularInline):
    model = InventorySetting
    extra = 1


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company',)
    search_fields = ('name',)
    inlines = [InventorySettingInline, ItemInline]

    def item_count(self, obj):
        return obj.items.count()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    list_filter = ('inventory__company', 'inventory')
    search_fields = ('name', 'description')
    inlines = [ItemDetailInline]


@admin.register(ItemDetail)
class ItemDetailAdmin(admin.ModelAdmin):
    list_display = ('item', 'setting', 'value')
    list_filter = ('item__inventory__company',)
    search_fields = ('setting_key', 'value')


@admin.register(InventorySetting)
class InventorySettingAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'key', 'type', 'allow_multiple')
    list_filter = ('inventory__company',)
    search_fields = ('key',)
