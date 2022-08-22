from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


def filename(instance, filename):
    return '/'.join(['recipes', str(instance.id), filename])


class Tag(models.Model):
    """Модель класса тег."""
    title = models.CharField('Название', max_length=255, unique=True)
    slug = models.SlugField('Сокращенное название', unique=True)
    color = ColorField(default='#49B64E', verbose_name='Цвет', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title[:30]


class Ingredient(models.Model):
    """Модель класса ингридиент."""
    UNIT_CHOICES = [
        ('грамм', 'гр.'),
        ('килограмм', 'кг.'),
        ('миллилитр', 'мл.'),
        ('литр', 'л.'),
        ('штука', 'шт.'),
        ('столовая ложка', 'ст. л.'),
        ('чайная ложка', 'ч. л.'),
        ('упаковка', 'уп.'),
        ('порция', 'порц.'),
        ('бутылка', 'бут.'),
    ]
    title = models.CharField('Название', max_length=255)
    amount = models.IntegerField(
        'Количество', validators=[MinValueValidator(1)])
    measure_unit = models.CharField(
        'Единица измерения', choices=UNIT_CHOICES, default='грамм',
        max_length=max(len(unit) for unit, _ in UNIT_CHOICES))

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title[:30]


class Recipe(models.Model):
    """Модель класса рецепт."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    duration = models.IntegerField(
        'Длительность', validators=[
            MinValueValidator(1), MaxValueValidator(500)])
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    image = models.ImageField(
        'Картинка', upload_to=filename, blank=True, )
    # default='no_image.png',
    ingredient = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        related_name='ingredients', verbose_name='Ингредиенты')
    tag = models.ManyToManyField(
        Tag, through='RecipeTag', related_name='tags', verbose_name='Теги')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title[:30]

    def get_ingredients(self):
        return '\n'.join([ing.title for ing in self.ingredient.all()])

    def get_tags(self):
        return '\n'.join([tag.title for tag in self.ingredient.all()])

    get_ingredients.short_description = 'Ингредиенты'
    get_tags.short_description = 'Теги'


class RecipeIngredient(models.Model):
    """Класс модели связи между рецептами и ингредиентами."""
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.ingredient} входит в состав {self.recipe}.'


class RecipeTag(models.Model):
    """Класс модели связи между рецептами и тегами."""
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.tag} относится к {self.recipe}.'
