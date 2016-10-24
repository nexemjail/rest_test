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
    UserListSerializer
)


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        return User.objects.get(pk=int(self.kwargs['id']))


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserLoginAPIView(views.APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                login(request, user)
                return response.Response({'detail': 'login successful'}, status.HTTP_200_OK)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return response.Response({'detail': 'log out successful'}, status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
