from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Recipe, Menu
from .forms import MenuForm


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


@login_required
def profile(request):
    current_menu = Menu.objects.get(client=request.user)
    number_of_meals = sum([
        current_menu.with_breakfasts,
        current_menu.with_lunches,
        current_menu.with_suppers,
        current_menu.with_desserts,
    ])
    context = {
        'menu': current_menu,
        'number_of_meals': number_of_meals,
    }
    return render(request, 'lk.html', context)


def order(request):
    if request.method == "POST":
        order_form = MenuForm(request.POST)
        if order_form.is_valid():
            menu_order = order_form.save(commit=False)
            menu_order.client = request.user
            menu_order.save()
            return redirect('profile')
        else:
            print(order_form.errors.as_data())
    else:
        order_form = MenuForm()
        context = {
            'order_form': order_form
        }
    return render(request, 'order.html', context)


def menu(request):
    days = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    ]
    client = request.user
    current_menu = Menu.objects.get(client=client)
    types_of_meal = {
        'breakfast': current_menu.with_breakfasts,
        'lunch': current_menu.with_lunches,
        'supper': current_menu.with_suppers,
        'dessert': current_menu.with_desserts,
    }
    possible_recipes = Recipe.objects.filter(

    )
    week_menu = []
    context = {
        'menu': current_menu,
        'week': days,
        'types_of_meal': types_of_meal,
    }
    return render(request, 'menu.html', context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})
