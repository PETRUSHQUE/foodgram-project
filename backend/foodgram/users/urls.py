from django.urls import include, path
from djoser.urls.authtoken import urlpatterns as token_urlpatterns
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet, UserViewSet, subscribe

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(
    r'^users/(?P<user_id>\d+)/subscriptions/', SubscriptionViewSet,
    basename='subscription')

urlpatterns = [
    path('auth/', include(token_urlpatterns)),
    path('users/<pk:int>/subscribe/', subscribe, name='subscribe'),
    path('', include(router_v1.urls)),
]
