from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id, *args, **kwargs):
        user_id = int(id)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user.exists():
                return response.Response(UserListSerializer(user.get()).data, status=status.HTTP_200_OK)
            return response.Response(data={'detail': 'no such user'}, status=status.HTTP_404_NOT_FOUND)
        return response.Response({'detail': 'invalid format'}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


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
                return response.Response(data={'detail': 'login successful'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return response.Response(data={'detail': 'log out successful'}, status=status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
