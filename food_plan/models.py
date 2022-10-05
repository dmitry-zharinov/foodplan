from django.db import models


class Menu(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

    def __str__(self):
        return self.name


class Allergen(models.Model):
    allergen_name = models.CharField('Название аллергена', max_length=200)

    class Meta:
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'

    def __str__(self):
        return self.allergen_name


class Unit(models.Model):
    name = models.CharField('Единица измерения продукта', max_length=50)

    class Meta:
        verbose_name = 'Единица измерения продукта'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=200)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        verbose_name='Единица измерения',
        null=True)

    allergen = models.ForeignKey(
        Allergen,
        on_delete=models.SET_NULL,
        verbose_name='Аллерген',
        null=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField('Название рецепта', max_length=200)
    description = models.TextField(
        blank=True,
        verbose_name='Краткое описание')
    instructions = models.TextField(
        verbose_name='Инструкция приготовления')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты в рецепте')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title
