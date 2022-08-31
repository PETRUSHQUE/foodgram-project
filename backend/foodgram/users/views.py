from djoser.views import UserViewSet
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes

from .paginators import PageLimitPagination
from .serializers import SubscriptionSerializer


class UserViewSet(UserViewSet):
    """Класс-контроллер для модели пользователя."""
    pagination_class = PageLimitPagination

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


class SubscriptionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Класс-контроллер для получения списка модели подписок."""
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )
    search_fields = ('subscribing__username', )

    def get_queryset(self):
        return self.request.user.subscriber.all()


@api_view(['POST', 'DELETE', ])
@permission_classes(permissions.IsAuthenticated)
def subscribe(request):
    """Контроллер подписки/отписки."""
    pass
