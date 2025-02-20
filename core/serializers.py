from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = get_user_model()
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
