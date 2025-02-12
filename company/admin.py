from django.contrib import admin
from . import models


@admin.register(models.Company)  # This registers the model.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


# Register your models here.
# admin.site.register(models.Company)
