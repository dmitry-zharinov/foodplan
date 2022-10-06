from django.contrib.auth.models import User
from django.db import models

PERIOD_CHOICES = [
    ('3', '3 мес.'),
    ('12', '12 мес.'),
]

RECIPE_TYPE = [
    ('breakfast', 'завтрак'),
    ('lunch', 'обед'),
    ('supper', 'ужин'),
    ('dessert', 'десерт'),
]


class Menu(models.Model):
    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    period = models.CharField(
        'Срок подписки',
        max_length=10,
        choices=PERIOD_CHOICES,
        default='3',
    )
    calories_per_day = models.IntegerField(
        'Калорий в день (всего)',
        default=0,
    )
    with_breakfasts = models.BooleanField(
        'Завтраки',
        default=True,
    )
    with_lunches = models.BooleanField(
        'Обеды',
        default=True,
    )
    with_suppers = models.BooleanField(
        'Ужины',
        default=True,
    )
    with_desserts = models.BooleanField(
        'Десерты',
        default=True,
    )
    persons = models.IntegerField(
        'Количество персон',
        default=1,
    )
    allergens = models.ManyToManyField(
        'Allergen',
        verbose_name='Исключить аллергены',
        related_name='in_menus',
        blank=True,
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return f'Меню для {self.client}'


class Recipe(models.Model):
    title = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    description = models.TextField(
        'Краткое описание',
        blank=True,
    )
    instructions = models.TextField(
        'Инструкция приготовления',
        blank=True,
    )
    type = models.CharField(
        'Тип блюда',
        max_length=10,
        choices=RECIPE_TYPE,
        default='breakfast',
    )
    calories = models.IntegerField(
        'Количество кКал',
    )
    image = models.ImageField(
        'Картинка',
        blank=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        related_name='in_recipes',
        blank=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    amount = models.DecimalField(
        'Количество',
        max_digits=6,
        decimal_places=2,
        default=1,
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='ingredients',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.product}, {self.amount}"


class Product(models.Model):
    title = models.CharField(
        'Название',
        max_length=120,
        db_index=True,
    )
    price = models.DecimalField(
        'Цена за штуку',
        max_digits=6,
        decimal_places=2,
        blank=True,
    )
    unit = models.ForeignKey(
        'Unit',
        on_delete=models.SET_NULL,
        verbose_name='Единицы измерения',
        related_name='of_products',
        null=True,
        blank=True,
    )
    allergen = models.ForeignKey(
        'Allergen',
        on_delete=models.SET_NULL,
        verbose_name='Название аллергена',
        related_name='products',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Allergen(models.Model):
    name = models.CharField(
        'Название аллергена',
        max_length=120,
        db_index=True,
        default='',
    )

    class Meta:
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(
        'Единица измерения продукта',
        max_length=50,
        blank=True,
    )
    short_name = models.CharField(
        'Сокращение',
        max_length=20,
        blank=True,
    )

    class Meta:
        verbose_name = 'Единица измерения продукта'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.short_name
