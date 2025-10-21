from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = User.objects.create_user(username=username, password=password)
        # mark inactive and generate code
        user.generate_confirmation_code()
        # create token but token will be used only after confirmation/login
        Token.objects.create(user=user)
        return user


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
        if user.confirmation_code != code:
            raise serializers.ValidationError('Invalid confirmation code')
        attrs['user'] = user
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User not active. Confirm first.')
        attrs['user'] = user
        return attrs
