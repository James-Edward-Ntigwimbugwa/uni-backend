from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Message
 
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'is_staff', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'profile_photo': {'required': False}
        }

    def create(self, validated_data):
        # If username not provided, the UserManager will handle setting it
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data.get('is_staff', False)
        )
        return user
      
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_photo']
        extra_kwargs = { 
            'profile_photo': {'required': True}
        }
        
    def update(self, instance, validated_data):
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.save()
        return instance
    
class MessageSerializer(serializers.Serializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True))
    # No recipient field needed, as all users can see the message
    body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Message.objects.create(**validated_data)