from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id', 'user_id', 'username', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class TelegramUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = TelegramUser
        fields = ['user_id', 'username', 'first_name', 'last_name']

    def validate_user_id(self, value):
        """Проверка уникальности user_id"""
        if TelegramUser.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("Пользователь с таким ID уже существует")
        return value