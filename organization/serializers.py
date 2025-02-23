from rest_framework import serializers
from .models import Profile, Company
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(
        source='user.last_name', read_only=True)
    companies = serializers.SerializerMethodField()  # Add companies field

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'phone_number',
                  'country', 'state', 'city', 'postal_code', 'companies']

    def get_companies(self, obj):
        # Fetch companies associated with the profile
        companies = obj.companies.all()
        return [{'id': company.id, 'name': company.name} for company in companies]


class CompanySerializer(serializers.ModelSerializer):
    profile_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'profile_count']

    def get_profile_count(self, obj):
        # Count profiles linked to this company via ProfileCompanyRole
        return obj.members.count()
