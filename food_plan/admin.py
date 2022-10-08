from django.contrib import admin
from .models import Menu, Allergen, Ingredient, Recipe


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
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


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
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


# class IngredientsInline(admin.TabularInline):
#     model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'type',
        'calories',
        'image',
    ]
    exclude = ['ingredients']
    search_fields = ['title']
    list_editable = ['type']
    list_filter = [
        'type',
    ]

    # inlines = [
    #     IngredientsInline,
    # ]
