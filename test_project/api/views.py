from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework import viewsets, generics, views, status
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import  Response
from serializers import UserLoginSerializer, UserCreateSerializer


class UserLoginAPIView(views.APIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                login(request, user)
                return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
