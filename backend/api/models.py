from django.db import models
from django.utils.html import format_html
from users.models import User


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Наименование ингридиента',
        max_length=200,
        unique=True,
    )
    dimension = models.CharField(
        verbose_name='Ед. изм.',
        max_length=200,
        help_text='Укажите единицу измерения',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug тэга')
    hex_color = models.CharField(
        max_length=200,
        default="#E26C2D",
        verbose_name='Цветовой HEX-код',
        blank=True)

    class Meta:
        verbose_name = 'Тэг'

    def __str__(self):
        return self.name

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hex_color,
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipes',
        verbose_name='Автор публикации')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        verbose_name="Изображение блюда",
        upload_to='recipes')
    text = models.TextField(
        max_length=5000,
        verbose_name='Текстовое описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        blank=True,
        related_name='recipes',)    
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент в рецепте')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(
        null=True,
        verbose_name='Количество ингредиента')

    class Meta:
        verbose_name = 'Ингредиент для рецепта'

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Покупка')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Покупка'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name='Рецепт')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} added {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписываемся')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_follow')]

    def __str__(self):
        return f'{self.user} => {self.author}'
