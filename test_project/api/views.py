from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from rest_framework import (
    permissions,
    generics,
    views,
    status,
    response
)
from serializers import (
    UserLoginSerializer,
    UserCreateSerializer,
    UserSerializer
)


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, pk=int(self.kwargs['id']))


class UserLoginAPIView(views.APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=request.data['username'],
                                password=request.data['password'])
            if user:
                login(request, user)
                return response.Response({'datail': 'login successful'}, status.HTTP_200_OK)
            return response.Response({'datail': 'user not exist or invalid credentials'}, status.HTTP_401_UNAUTHORIZED)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return response.Response({'datail': 'log out was successful'}, status.HTTP_200_OK)

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return response.Response({'datail': 'user already exists'}, status.HTTP_409_CONFLICT)
            self.perform_create(serializer)
            return response.Response({'datail': 'user created'}, status.HTTP_201_CREATED)
        return response.Response({'datail': 'invalid data format'}, status.HTTP_400_BAD_REQUEST)

