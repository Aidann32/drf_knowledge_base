from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from eth_utils import is_checksum_address
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser as User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password



class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        wallet_address = request.data.get('wallet_address')
        if wallet_address:
            if not is_checksum_address(wallet_address):
                return Response(
                    {"error": "Invalid wallet address. Please provide a valid Ethereum address."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user_id": user.id}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginAPIView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Проверка наличия обязательных полей
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Создание или получение токена для пользователя
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Login successful.",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "wallet_address": user.wallet_address,
                },
            },
            status=status.HTTP_200_OK
        )

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получение текущего пользователя
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "wallet_address": user.wallet_address,
                "date_joined": user.date_joined,
            },
            status=status.HTTP_200_OK
        )
        
class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # Обновление username
        username = data.get('username')
        if username:
            user.username = username

        # Обновление email
        email = data.get('email')
        if email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response(
                    {"error": "Email is already in use."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.email = email

        # Обновление пароля
        password = data.get('password')
        if password:
            user.password = make_password(password)

        # Обновление wallet_address (если разрешено менять)
        wallet_address = data.get('wallet_address')
        if wallet_address:
            if not is_checksum_address(wallet_address):
                return Response(
                    {"error": "Invalid wallet address. Please provide a valid Ethereum address."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(wallet_address=wallet_address).exclude(id=user.id).exists():
                return Response(
                    {"error": "Wallet address is already in use."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.wallet_address = wallet_address

        # Сохранение изменений
        user.save()

        return Response(
            {
                "message": "User updated successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "wallet_address": user.wallet_address,
                },
            },
            status=status.HTTP_200_OK,
        )