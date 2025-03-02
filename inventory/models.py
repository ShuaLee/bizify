from django.db import models
from organization.models import Company


class Inventory(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Item(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.inventory.name})"


class Attribute(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    name = models.CharField(max_length=255)
    field_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('url', 'URL'),
            ('bool', 'Boolean'),
        ],
        default='text'
    )
    allow_multiple = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.field_type})"

    class Meta:
        unique_together = ('inventory', 'name')


class ItemAttribute(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE
    )
    value = models.TextField()

    def __str__(self):
        return f"{self.attribute.name}: {self.value} ({self.item.name})"

    class Meta:
        unique_together = ('item', 'attribute')
