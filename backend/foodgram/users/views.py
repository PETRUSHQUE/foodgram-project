from api.pagination import PageLimitPagination
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers


class UserViewSet(UserViewSet):
    """Класс-контроллер для модели пользователя."""
    pagination_class = PageLimitPagination

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        """Метод эндпоинта с информацией о текущем пользователе."""
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=['post', 'delete'], detail=True,
        permission_classes=(permissions.IsAuthenticated, ))
    def subscribe(self, request, *args, **kwargs):
        """Метод эндпоинта подписки/отписки на автора."""
        author = get_object_or_404(models.User, id=kwargs['id'])
        if request.method == 'POST':
            data = request.data.copy()
            data.update({'author': author.id})
            serializer = serializers.SubscriptionSerializer(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=self.get_serializer(author).data)
        obj = request.user.subscriber.filter(author=author)
        if not obj.exists():
            return Response(
                {'errors': 'Вы не подписаны на данного автора.'},
                status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'], detail=False,
        permission_classes=(permissions.IsAuthenticated, ),
        serializer_class=serializers.SubscriptionInfoSerializer)
    def subscriptions(self, request, *args, **kwargs):
        """Метод эндпоинта подписок текущего пользователя."""
        queryset = request.user.subscriber.all()
        pages = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
