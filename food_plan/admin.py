from django.contrib import admin
from .models import Menu, Allergen, Unit, Ingredient, Recipe, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'unit',
        'allergen',
    ]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'type',
        'image',
    ]
    exclude = ['ingredients']
    search_fields = ['title']

    list_filter = [
        'type',
    ]

    inlines = [
        IngredientsInline,
    ]
