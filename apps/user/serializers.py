from rest_framework import serializers
from .models import CustomUser as User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'wallet_address')

    def create(self, validated_data):
        # Создание пользователя с хэшированным паролем
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            wallet_address=validated_data.get('wallet_address')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
