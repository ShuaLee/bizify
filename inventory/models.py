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
