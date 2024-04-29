from rest_framework import serializers
from user.models import User
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True)
    password2 = serializers.CharField(max_length=50, write_only=True)
    full_name = serializers.SerializerMethodField()    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2', 'full_name']

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']

        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        return user

    def validate_email(self,value):
        email = value
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already has been taken.')
        return value
    def validate_password(self, value):
        password = value
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, password):
            raise serializers.ValidationError('Password must be at least 8 characters long and contain at least one number, one uppercase, and one lowercase letter.')
        return value
    
    def get_full_name(self,instance):
        first_name = instance.first_name
        last_name = instance.last_name
        return first_name + " " + last_name

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError('Password and confirm Password must be the same.')

        return super().validate(attrs)
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=50, style={'input_type':'password'})
    
    def validate(self, attrs):
        return attrs


class VerifyEmailTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email_verification_token = serializers.CharField(max_length=2000)

    def validate(self, attrs):
        return attrs
    
class RefreshAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=2000)

    def validate(self, attrs):
        return super().validate(attrs)
    
class SendEmailVerificationAgainSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        return super().validate(attrs)
    

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)

    def validate_new_password(self, value):
        password = value
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, password):
            raise serializers.ValidationError('Password must be at least 8 characters long and contain at least one number, one uppercase, and one lowercase letter.')
        return value
    
    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        if old_password == new_password:
            raise serializers.ValidationError('Old password and new password must be different.')
        return super().validate(attrs)

