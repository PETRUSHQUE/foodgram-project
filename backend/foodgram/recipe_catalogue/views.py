from rest_framework import mixins, viewsets

from . import models, serializers


class ListRetrieveViewSet(
        mixins.ListModelMixin, mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """Базовый класс-контроллер с действиями получения списка и экземпляра."""


class TagViewSet(ListRetrieveViewSet):
    """Класс-контроллер модели тег."""
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(ListRetrieveViewSet):
    """Класс-контроллер модели ингредиент."""
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс-контроллер модели рецепт."""
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
