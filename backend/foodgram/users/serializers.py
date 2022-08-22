import rest_framework.serializers as serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import Subscription, User


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор класса подписок."""
    subscriber = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    subscribing = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscribing', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['subscriber', 'subscribing', ]
            )
        ]

    def validate_subscribing(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя дважды!'
            )
        return value


class UserInfoSerializer(UserSerializer):
    """Сериализатор класса пользователей."""

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', )
        read_only_fields = ('email', )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = self.context.get('request').user
        ret['is_subscribed'] = Subscription.objects.filter(
            user=user, author=instance).exists() if user.is_authenticated else False
        return ret


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор класса пользователей для регистрации."""

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )
