from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели тег."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели ингредиент."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class GetRecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатор модели рецепт."""

    class Meta:
        model = Recipe
        fields = '__all__'


class PostRecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатор модели рецепт."""

    class Meta:
        model = Recipe
        fields = '__all__'
