import rest_framework.mixins as mixins
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .paginators import PageLimitPagination
from .serializers import SubscriptionSerializer


class UserViewSet(UserViewSet):
    """Класс-контроллер для модели пользователя."""
    pagination_class = PageLimitPagination

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


class SubscriptionViewSet(
        GenericViewSet, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, mixins.ListModelMixin):
    """Класс-контроллер для модели подписок."""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )
    search_fields = ('subscribing__username', )

    def get_queryset(self):
        return self.request.user.subscriber.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
