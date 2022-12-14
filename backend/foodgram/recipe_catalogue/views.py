from api.pagination import PageLimitPagination
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import filters, models, pdf, serializers
from .permissions import IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс-контроллер модели тег."""
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс-контроллер модели ингредиент."""
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    filter_backends = (filters.IngredientFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс-контроллер модели рецепт."""
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    pagination_class = PageLimitPagination
    filter_class = filters.RecipeFilter
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create_obj(self, request, recipe):
        """Вспомогательный метод создания объекта избранного/списка покупок."""
        data = request.data.copy()
        data.update({'recipe': recipe.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializers.PartialRecipeSerializer(recipe).data,
            status=status.HTTP_201_CREATED)

    def del_obj(self, request, recipe, model):
        """Вспомогательный метод удаления объекта избранного/списка покупок."""
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if not obj.exists():
            return Response(
                {'errors': 'Рецепт отсутствует в избранном.'},
                status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'], detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
        serializer_class=serializers.FavoriteSerializer)
    def favorite(self, request, *args, **kwargs):
        """Метод эндпоинта добавления/удаления рецепта из списка избранного."""
        recipe = get_object_or_404(models.Recipe, id=kwargs['pk'])
        if request.method == 'POST':
            return self.create_obj(request, recipe)
        return self.del_obj(request, recipe, models.Favorite)

    @action(
        methods=['post', 'delete'], detail=True,
        permission_classes=(permissions.IsAuthenticated, ),
        serializer_class=serializers.ShoppingCartSerializer)
    def shopping_cart(self, request, *args, **kwargs):
        """Метод эндпоинта добавления/удаления рецепта из списка покупок."""
        recipe = get_object_or_404(models.Recipe, id=kwargs['pk'])
        if request.method == 'POST':
            return self.create_obj(request, recipe)
        return self.del_obj(request, recipe, models.ShoppingCart)

    @action(
        methods=['get'], detail=False,
        permission_classes=(permissions.IsAuthenticated, ))
    def download_shopping_cart(self, request):
        """Метод эндпоинта скачивания списка покупок PDF файлом."""
        ingredients = models.RecipeIngredient.objects.filter(
            recipe__shoppingcarts__user=request.user).values_list(
            'ingredient__name', 'amount', 'ingredient__measurement_unit')
        cart = {}
        for name, amount, unit in ingredients:
            if name not in cart:
                cart[name] = {'amount': amount, 'unit': unit}
            else:
                cart[name]['amount'] += amount
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf"')
        return pdf.pfd_table(response, cart)
