from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Класс админки для модели подписок."""
    model = Subscription
    list_display = ('author', 'user', )
    list_filter = ('author', 'user', )
    search_fields = ('author', 'user', )


@admin.register(User)
class UserAdmin(UserAdmin):
    """Класс админки для модели пользователя."""
    model = User
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', )
    list_filter = ('username', 'email', )
    search_fields = ('username', 'email', 'first_name', 'last_name', )
    empty_value_display = '-пусто-'
