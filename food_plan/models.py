from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    recipe_name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )

    added_date = models.DateTimeField(
        verbose_name='Дата добавления',
        default=timezone.now
    )
    modified_date = models.DateTimeField(
        verbose_name='Дата изменения',
        null=True
    )

    def __str__(self) -> str:
        return f"{self.recipe_name}"

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
