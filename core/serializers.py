from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
