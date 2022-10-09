from django.contrib import admin
from .models import Menu, Allergen, Ingredient, Recipe


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'client',
    )
    list_display = [
        'client',
        'period',
        'calories_per_day',
        'with_breakfasts',
        'with_lunches',
        'with_suppers',
        'with_desserts',
        'persons',
    ]


class IngredientsInLine(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'type',
        'calories',
        'image',
    ]
    search_fields = ['title']
    list_editable = ['type']
    list_filter = [
        'type',
    ]
    inlines = [
        IngredientsInLine,
    ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'recipe',
    )
    list_display = [
        'title',
        'amount',
        'unit',
        'price',
        'allergen',
    ]
    list_filter = [
        'unit',
        'allergen',
    ]


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    pass
