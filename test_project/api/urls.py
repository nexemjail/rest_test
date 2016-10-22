from django.conf.urls import url, include
from rest_framework import urls
from views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserListAPIView,
    UserDetailAPIView,
)

api_patterns = [
    url(r'(?P<id>[0-9]+)', UserDetailAPIView.as_view(), name='detail'),
    url(r'^login/', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/', UserCreateAPIView.as_view(), name='register'),
    url(r'^logout/', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^$', UserListAPIView.as_view())
]

urlpatterns = [

    url(r'^', include(api_patterns)),
    url(r'^auth/', include(urls, namespace='rest_framework')),
]