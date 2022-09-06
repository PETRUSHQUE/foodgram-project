from api.pagination import PageLimitPagination
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from . import models, serializers


class UserViewSet(UserViewSet):
    """Класс-контроллер для модели пользователя."""
    pagination_class = PageLimitPagination

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(['post', 'delete'], detail=True)
    @permission_classes(permissions.IsAuthenticated)
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(models.User, id=kwargs['id'])
        data = request.data.copy()
        data.update({'author': author.id})
        serializer = serializers.SubscriptionSerializer(
            data=data, context={'request': request})
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=self.get_serializer(author).data)
        return Response(status=status.HTTP_200_OK, data={'xd': 'xd'})

    @action(['get'], detail=False)
    @permission_classes(permissions.IsAuthenticated)
    def subscriptions(self, request):
        queryset = request.user.subscriber.all()
        pages = self.paginate_queryset(queryset)
        serializer = serializers.SubscriptionInfoSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
