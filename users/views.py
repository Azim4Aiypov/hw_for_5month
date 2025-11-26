import redis
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserLoginSerializer
from utils.confirmation import set_confirmation_code, get_confirmation_code, delete_confirmation_code

User = get_user_model()

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        code = set_confirmation_code(user.id)
        print("CONFIRM CODE:", code)


class UserConfirmView(generics.GenericAPIView):
    serializer_class = UserConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["confirmation_code"]

        user = User.objects.get(email=email)
        saved_code = get_confirmation_code(user.id)

        if not saved_code:
            return Response({"detail": "Code expired or not found"}, status=status.HTTP_400_BAD_REQUEST)

        if saved_code != code:
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        delete_confirmation_code(user.id)
        user.is_active = True
        user.is_confirmed = True
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"detail": "Confirmed", "token": token.key}, status=status.HTTP_200_OK)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
