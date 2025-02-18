from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Company)  # This registers the model.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
