from djoser.serializers import UserCreateSerializer, UserSerializer
from recipe_catalogue.serializers import GetRecipeSerializer
from rest_framework import serializers

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
                fields=['author', 'user', ]
            )
        ]

    def create(self, validated_data):
        return models.Subscription.objects.create(
            user=self.context.get('request').user, **validated_data)

    def validate_subscribing(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя дважды!')
        return value


class SubscriptionInfoSerializer(serializers.ModelSerializer):
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
        return models.Subscription.objects.filter(
            user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return GetRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
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
        user = self.context.get('request').user
        return models.Subscription.objects.filter(
            user=user, author=obj.id
        ).exists() if user.is_authenticated else False


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор класса пользователей для регистрации."""

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )
