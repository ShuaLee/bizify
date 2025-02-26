from django.db import models
from organization.models import Company

# Create your models here.


class Inventory(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='inventories')
    name = models.CharField(max_length=150)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class InventorySetting(models.Model):
    VALUE_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('url', 'URL'),
        ('bool', 'Boolean'),
    )

    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="settings")
    key = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=VALUE_TYPES, default='text')
    allow_multiple = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.key} ({self.type}) - {self.inventory.name}"

    class Meta:
        # One setting per key per inventory
        unique_together = ('inventory', 'key')


class Item(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.inventory.name})"


class ItemDetail(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='details')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.key}: {self.value} ({self.item.name})"
