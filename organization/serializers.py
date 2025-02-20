from rest_framework import serializers
from .models import Company, Profile
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'first_name']


class CompanySerializer(serializers.ModelSerializer):
    members = ProfileSerializer(many=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'members']
