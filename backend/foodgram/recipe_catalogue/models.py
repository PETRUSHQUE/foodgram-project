from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель класса тег."""
    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.SlugField('Сокращенное название', unique=True)
    color = ColorField(default='#49B64E', verbose_name='Цвет', unique=True)

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:30]


class Ingredient(models.Model):
    """Модель класса ингридиент."""
    UNIT_CHOICES = [
        ('г', 'г'),
        ('кг', 'кг'),
        ('мл', 'мл'),
        ('л', 'л'),
        ('шт.', 'шт.'),
        ('ст. л.', 'ст. л.'),
        ('ч. л.', 'ч. л.'),
        ('упаковка', 'упаковка'),
        ('пачка', 'пачка'),
        ('бутылка', 'бутылка'),
        ('пакет', 'пакет'),
        ('пакетик', 'пакетик'),
        ('по вкусу', 'по вкусу'),
        ('кусок', 'кусок'),
        ('стакан', 'стакан'),
        ('банка', 'банка'),
        ('горсть', 'горсть'),
        ('щепотка', 'щепотка'),
        ('веточка', 'веточка'),
        ('стебель', 'стебель'),
        ('капля', 'капля'),
        ('пучок', 'пучок'),
        ('лист', 'лист'),
        ('стручок', 'стручок'),
        ('тушка', 'тушка'),
        ('звездочка', 'звездочка'),
        ('порция', 'порция'),
        ('батон', 'батон'),
        ('ломтик', 'ломтик'),
    ]
    name = models.CharField('Название', max_length=255)
    measurement_unit = models.CharField(
        'Единица измерения', choices=UNIT_CHOICES, default='г',
        max_length=max(len(unit) for unit, _ in UNIT_CHOICES))

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:30]


class Recipe(models.Model):
    """Модель класса рецепт."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.IntegerField(
        'Длительность приготовления', validators=[MinValueValidator(1)])
    image = models.ImageField('Картинка', upload_to='recipe', blank=True, )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        related_name='recipes', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:30]

    def get_ingredients(self):
        return '\n'.join([ing.name for ing in self.ingredients.all()])

    def get_tags(self):
        return '\n'.join([tag.name for tag in self.tags.all()])

    get_ingredients.short_description = 'Ингредиенты'
    get_tags.short_description = 'Теги'


class RecipeIngredient(models.Model):
    """Класс модели связи между рецептами и ингредиентами."""
    recipe = models.ForeignKey(
        Recipe, related_name='recipeingredients',
        on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey(
        Ingredient, related_name='recipeingredients',
        on_delete=models.SET_NULL, null=True)
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[MinValueValidator(1)])

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe', ),
                name='unique_ingredients_recipe')
        ]

    def __str__(self):
        return f'{self.ingredient} входит в состав {self.recipe}.'


class BaseFavorite(models.Model):
    """Базовый класс избранных рецептов."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='%(class)ss', verbose_name='Рецепт')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)ss', verbose_name='Пользователь')

    class Meta:
        abstract = True
        ordering = ('-id', )


class Favorite(BaseFavorite):
    """Класс модели избранных рецептов."""

    class Meta(BaseFavorite.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe', ), name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}.'


class ShoppingCart(BaseFavorite):
    """Класс модели списка покупок."""

    class Meta(BaseFavorite.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe', ), name='unique_cart')
        ]

    def __str__(self):
        return f'{self.recipe} в корзине покупок у {self.user}.'
