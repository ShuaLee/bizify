from django.conf import settings
from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
    companies = models.ManyToManyField(
        Company, through='ProfileCompanyRole', related_name='members')

    # Magic methods
    def __str__(self):
        return self.user.email


class Role(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=150)
    permissions = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    class Meta:
        unique_together = ('company', 'name')


class ProfileCompanyRole(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.email} - {self.company.name}"
