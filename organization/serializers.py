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
    profiles = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'profiles']

    def get_profiles(self, obj):
        # Fetch profiles linked to the company via ProfileCompanyRole
        profiles = obj.members.all()
        return [{'id': profile.id, 'email': profile.user.email} for profile in profiles]
