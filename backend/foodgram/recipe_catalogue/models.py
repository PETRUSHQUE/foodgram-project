from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


def filename(instance, filename):
    return '/'.join(['recipes', str(instance.id), filename])


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
        ('грамм', 'г'),
        ('килограмм', 'кг'),
        ('миллилитр', 'мл'),
        ('литр', 'л'),
        ('штука', 'шт.'),
        ('столовая ложка', 'ст. л.'),
        ('чайная ложка', 'ч. л.'),
        ('упаковка', 'упаковка'),
        ('порция', 'порц.'),
        ('бутылка', 'бутылка'),
        ('пакет', 'пакет'),
        ('по вкусу', 'по вкусу'),
        ('кусок', 'кусок'),
        ('стакан', 'стакан'),
        ('банка', 'банка'),
        ('горсть', 'горсть'),
    ]
    name = models.CharField('Название', max_length=255)
    measurement_unit = models.CharField(
        'Единица измерения', choices=UNIT_CHOICES, default='гр.',
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
    description = models.TextField('Описание')
    duration = models.IntegerField(
        'Длительность', validators=[MinValueValidator(1)])
    image = models.ImageField(
        'Картинка', upload_to=filename, blank=True, )
    # default='no_image.png',
    ingredient = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        related_name='ingredients', verbose_name='Ингредиенты')
    tag = models.ManyToManyField(Tag, related_name='tags', verbose_name='Теги')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:30]

    def get_ingredients(self):
        return '\n'.join([ing.name for ing in self.ingredient.all()])

    def get_tags(self):
        return '\n'.join([tag.name for tag in self.ingredient.all()])

    get_ingredients.short_description = 'Ингредиенты'
    get_tags.short_description = 'Теги'


class RecipeIngredient(models.Model):
    """Класс модели связи между рецептами и ингредиентами."""
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[MinValueValidator(1)])

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.ingredient} входит в состав {self.recipe}.'


# class RecipeTag(models.Model):
#     """Класс модели связи между рецептами и тегами."""
#     recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
#     tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name = 'Теги рецепта'
#         verbose_name_plural = 'Теги рецептов'

#     def __str__(self):
#         return f'{self.tag} относится к {self.recipe}.'


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
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_%(class)ss')
        ]


class Favorite(BaseFavorite):
    """Класс модели избранных рецептов."""

    class Meta(BaseFavorite.Meta):
        ordering = ('-id', )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}.'


class ShoppingCart(BaseFavorite):
    """Класс модели списка покупок."""

    class Meta(BaseFavorite.Meta):
        ordering = ('-id', )
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.recipe} в корзине покупок у {self.user}.'
