from django.conf.urls import url, include
from rest_framework import routers, urls as rest_urls
from views import UserCreateAPIView, UserLoginAPIView, UserLogoutAPIView

api_patterns = [
    url(r'^login/', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/', UserCreateAPIView.as_view(), name='register'),
    url(r'^logout/', UserLogoutAPIView.as_view(), name='logout'),
]

urlpatterns = [
    url(r'^user/', include(api_patterns)),
    url(r'^auth/', include(rest_urls, namespace='rest_framework')),
]