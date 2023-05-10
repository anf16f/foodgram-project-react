from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Тэг',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug Тега',
    )
    color = models.CharField(max_length=7)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=116,
        unique=True,
        blank=False,
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=11,
        verbose_name='единицы измерения',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=256,
        verbose_name='Рецепт',
        help_text='Название рецепта',
    )
    text = models.TextField(
        null=False,
        blank=False,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Теги',
        help_text='Теги',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='RecipeIngredient',
        verbose_name='Рецепт',
        help_text='Название рецепта',
    )
    cooking_time = models.DurationField(
        blank=False,
        null=False,
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=False,
        blank=False,
        verbose_name='Изображение',
        help_text='Изображение',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}: {self.text[15:]}...'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_RecipeIngredient",
                fields=['recipe', 'ingredient'],
            ),
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='on_recipes'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='on_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_RecipeTags",
                fields=['recipe', 'tag'],
            ),
        ]


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в корзину продуктов',
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_ShopingCart",
                fields=['user', 'recipe'],
            ),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в избранное',
        on_delete=models.DO_NOTHING,
        related_name='favorites',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_Favorites",
                fields=['user', 'recipe'],
            ),
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка на автора:',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_Subscribe",
                fields=['user', 'following'],
            ),
        ]
