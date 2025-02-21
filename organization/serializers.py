from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(
        source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'phone_number',
                  'country', 'state', 'city', 'postal_code', 'address']
