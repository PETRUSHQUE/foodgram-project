from django.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор класса подписок."""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Subscription
        fields = ('author', 'user', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Subscription.objects.all(),
                fields=('author', 'user', ))]

    def create(self, validated_data):
        return models.Subscription.objects.create(
            user=self.context.get('request').user, **validated_data)

    def validate_author(self, value):
        """Метод валидации поля автор."""
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя!')
        return value


class SubscriptionInfoSerializer(serializers.ModelSerializer):
    """Класс-сериализатор модели подписок для вывода информации о подписке."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Метод проверки подписки пользователя на автора."""
        return models.Subscription.objects.filter(
            user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        """Метод вывода рецептов автора."""
        from recipe_catalogue.serializers import PartialRecipeSerializer
        request = self.context.get('request')
        recipes_limit = request.query_params.get(
            'recipes_limit', settings.PAGE_SIZE)
        queryset = obj.author.recipes.all()[:int(recipes_limit)]
        return PartialRecipeSerializer(
            queryset, many=True).data

    def get_recipes_count(self, obj):
        """Метод вывода количества рецептов автора."""
        return obj.author.recipes.count()


class UserInfoSerializer(UserSerializer):
    """Сериализатор класса пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')
        read_only_fields = ('email', )

    def get_is_subscribed(self, obj):
        """Метод проверки подписки пользователя на автора."""
        user = self.context.get('request').user
        return user.is_authenticated and models.Subscription.objects.filter(
            user=user, author=obj.id).exists()


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор класса пользователей для регистрации."""
    email = serializers.EmailField(
        max_length=255,
        validators=[UniqueValidator(queryset=models.User.objects.all())])
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=models.User.objects.all())])

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )
