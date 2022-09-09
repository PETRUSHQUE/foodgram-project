from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models


class BaseFavoriteSerializer(serializers.ModelSerializer):
    """Базовый класс-сериализатор списка избранного."""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())


class FavoriteSerializer(BaseFavoriteSerializer):
    """Класс-сериализатор модели списка избранного."""

    class Meta:
        model = models.Favorite
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Favorite.objects.all(),
                fields=('recipe', 'user', )
            )
        ]

    def create(self, validated_data):
        return models.Favorite.objects.create(
            user=self.context.get('request').user, **validated_data)


class ShoppingCartSerializer(BaseFavoriteSerializer):
    """Класс-сериализатор модели корзины покупок."""

    class Meta:
        model = models.ShoppingCart
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.ShoppingCart.objects.all(),
                fields=('recipe', 'user', )
            )
        ]

    def create(self, validated_data):
        return models.ShoppingCart.objects.create(
            user=self.context.get('request').user, **validated_data)


class TagSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели тег."""

    class Meta:
        model = models.Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели ингредиент."""

    class Meta:
        model = models.Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели связи ингредиентов и рецептов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    amount = serializers.IntegerField(min_value=1)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit', )
        validators = [
            UniqueTogetherValidator(
                queryset=models.RecipeIngredient.objects.all(),
                fields=('ingredient', 'recipe', )
            )
        ]


class PartialRecipeSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели рецептов для получения части данных о них."""
    image = Base64ImageField()

    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )
        read_only_fields = ('id', 'name', 'image', 'cooking_time', )


class RecipeSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели рецепт для создания и изменения."""
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredients', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time', )

    def get_author(self, obj):
        """Метод получения информации об авторе рецепта."""
        # Пришлось импортировать здесь, иначе ошибка циклическового
        # импортирования сериализаторов из одного модуля в другой
        from users.serializers import UserInfoSerializer
        return UserInfoSerializer(
            obj.author, read_only=True,
            context={'request': self.context.get('request')}).data

    def get_is_favorited(self, obj):
        """Метод получения информации о том, является ли рецепт избранным."""
        user = self.context.get('request').user
        return user.is_authenticated and (
            user.favorites.filter(recipe__id=obj.id).exists())

    def get_is_in_shopping_cart(self, obj):
        """Метод получения информации о том, находится ли рецепт в корзине."""
        user = self.context.get('request').user
        return user.is_authenticated and (
            user.shoppingcarts.filter(recipe__id=obj.id).exists())

    def create_ingredients(self, ingredients, recipe):
        """
        Вспомогательный метод создания объектов
        связанной модели ингредиенты рецепта.
        """
        for ingredient in ingredients:
            models.RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        recipe = models.Recipe.objects.create(**validated_data)
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        self.create_ingredients(self.initial_data.get('ingredients'), recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.tags.clear()
        instance.tags.set(self.initial_data.get('tags'))
        instance.recipeingredients.all().delete()
        self.create_ingredients(self.initial_data.get('ingredients'), instance)
        instance.save()
        return instance
