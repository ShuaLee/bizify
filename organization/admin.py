from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'company_list', 'role_list']
    search_fields = ('user__email', 'phone_number')
    list_filter = ('companies',)  # Filter by companies

    def company_list(self, obj):
        # Display all companies as a comma-separated string
        companies = obj.companies.all()
        return ", ".join(company.name for company in companies) if companies else "None"
    company_list.short_description = 'Companies'

    def role_list(self, obj):
        # Display roles from ProfileCompanyRole
        profile_roles = models.ProfileCompanyRole.objects.filter(profile=obj)
        return ", ".join(str(profile_role.role) if profile_role.role else "No Role" for profile_role in profile_roles) if profile_roles else "None"
    role_list.short_description = 'Roles'


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at',]
    search_fields = ['name', 'description']


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company',)
    search_fields = ('name',)


@admin.register(models.ProfileCompanyRole)
class ProfileCompanyRoleAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'role')
    list_filter = ('company', 'role')
    search_fields = ('profile__user__email', 'company__name')
