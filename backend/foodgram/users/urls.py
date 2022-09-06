from django.urls import include, path
from djoser.urls.authtoken import urlpatterns as token_urlpatterns
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include(token_urlpatterns)),
    path('', include(router_v1.urls)),
]
