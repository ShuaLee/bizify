from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'user__first_name', 'user__last_name']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'admin_count']
    list_filter = ['created_at',]
    search_fields = ['name', 'description']
    filter_horizontal = ['admins',]

    def admin_count(self, obj):
        return obj.admins.count()

    admin_count.short_description = 'Number of Admins.'
