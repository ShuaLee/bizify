from django.contrib import admin
from .models import Company, ProfileCompanyRole, Profile, Role


# Register your models here.
class ProfileCompanyRoleInline(admin.TabularInline):
    model = ProfileCompanyRole
    extra = 1  # Number of empty rows to add by default
    fields = ('profile', 'company', 'role')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'company_list', 'role_list']
    search_fields = ('user__email', 'phone_number')
    list_filter = ('companies',)  # Filter by companies
    readonly_fields = ['company_list', 'role_list']  # Add to detail page
    inlines = [ProfileCompanyRoleInline]

    def company_list(self, obj):
        # Display all companies as a comma-separated string
        companies = obj.companies.all()
        return ", ".join(company.name for company in companies) if companies else "None"
    company_list.short_description = 'Companies'

    def role_list(self, obj):
        # Display roles and their associated companies from ProfileCompanyRole
        profile_roles = ProfileCompanyRole.objects.filter(profile=obj)
        return ", ".join(
            f"{profile_role.role.name} ({profile_role.company.name})"
            if profile_role.role else f"No Role ({profile_role.company.name})"
            for profile_role in profile_roles
        ) if profile_roles else "None"
    role_list.short_description = 'Roles'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'profile_count']
    list_filter = ['created_at',]
    search_fields = ['name', 'description']
    inlines = [ProfileCompanyRoleInline]

    def profile_count(self, obj):
        return obj.members.count()
    profile_count.short_description = 'Number of Profiles'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company',)
    search_fields = ('name',)


@admin.register(ProfileCompanyRole)
class ProfileCompanyRoleAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'role')
    list_filter = ('company', 'role')
    search_fields = ('profile__user__email', 'company__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            # Get the current object's company if editing, or None if creating
            if request.resolver_match.kwargs.get('object_id'):
                obj = self.get_object(
                    request, request.resolver_match.kwargs['object_id'])
                if obj and obj.company:
                    kwargs['queryset'] = Role.objects.filter(
                        company=obj.company)
            # if company is selected int he form (via POST), filter roles by that
            elif request.POST.get('company'):
                kwargs['queryset'] = Role.objects.filter(
                    company_id=request.POST['company'])
            else:
                # No roles until company is picked
                kwargs['queryset'] = Role.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
