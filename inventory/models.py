from django.db import models
from organization.models import Company

# Create your models here.


class Inventory(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='inventories')
    name = models.CharField(max_length=150)
    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Format: {'key': {'type': 'text|number|url|bool', 'allow_multiple': true|false}}"
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Item(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Key-value pairs matching inventory settings (e.g., {'part_no': 'ABC123', 'price': '5.99'})"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.inventory.name})"
