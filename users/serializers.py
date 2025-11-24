from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from utils.confirmation import get_confirmation_code, delete_confirmation_code

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'birthdate']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.generate_confirmation_code()
        user.save()
        Token.objects.create(user=user)
        return user

class UserConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('confirmation_code')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
        real_code = get_confirmation_code(user.id)
        if real_code != code:
            raise serializers.ValidationError('Invalid confirmation code')
        delete_confirmation_code(user.id)
        user.is_active = True
        user.is_confirmed = True
        user.save()
        attrs['user'] = user
        return attrs

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User not active. Confirm first.')
        attrs['user'] = user
        return attrs
