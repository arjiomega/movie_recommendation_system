from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'avatar_path']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'username': {'required': False}  # Make sure username is not required
        }

    def create(self, validated_data):
        # Automatically generate username from email
        email = validated_data['email']
        username = email.split('@')[0]  # Set username as the part before '@' in email
        validated_data['username'] = username  # Add the generated username to validated data
        
        # Create the user
        user = CustomUser.objects.create_user(**validated_data)  # Use create_user to handle password hashing
        return user

    # def create(self, validated_data):
    #     # Use create_user to handle password hashing
    #     user = CustomUser.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         avatar_path=validated_data.get('avatar_path', ''),
    #     )
    #     return user

    