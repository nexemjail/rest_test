from django.conf.urls import url, include
from rest_framework import routers, urls as rest_urls
from views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'auth/', include(rest_urls, namespace='rest_framework')),
]