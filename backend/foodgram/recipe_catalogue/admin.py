from django.contrib import admin

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс админки для модели рецептов."""
    model = models.Recipe
    list_display = (
        'title', 'author', 'duration', 'get_ingredients',
        'get_tags', 'pub_date', )
    list_filter = ('title', 'author', 'pub_date', )
    search_fields = (
        'title', 'author', 'get_ingredients', 'get_tags', 'pub_date', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс админки для модели тегов."""
    model = models.Tag
    list_display = ('title', 'slug', 'color', )
    list_filter = ('title', 'slug', )
    search_fields = ('title', 'slug', )


@admin.register(models.RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    """Класс админки для модели связи тегов и рецептов."""
    model = models.RecipeTag
    list_display = ('recipe', 'tag', )
    list_filter = ('recipe', 'tag', )
    search_fields = ('recipe', 'tag', )


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс админки для модели пользователя."""
    model = models.Ingredient
    list_display = ('title', 'amount', 'measure_unit', )
    list_filter = ('title', 'amount', 'measure_unit', )
    search_fields = ('title', 'amount', 'measure_unit', )


@admin.register(models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Класс админки для модели связи ингредиентов и рецептов."""
    model = models.RecipeIngredient
    list_display = ('recipe', 'ingredient', )
    list_filter = ('recipe', 'ingredient', )
    search_fields = ('recipe', 'ingredient', )
