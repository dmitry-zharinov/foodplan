from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MenuForm
from .models import Menu, Recipe


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


@login_required
def profile(request):
    try:
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
    except Menu.DoesNotExist:
        context = {
            'menu': None,
            'number_of_meals': None,
        }
    return render(request, 'lk.html', context)


def order(request):
    context = {
        'client_id': getattr(settings, "PAYPAL_CLIENT_ID", None)
    }

    if request.method == "POST":
        order_form = MenuForm(request.POST)
        if order_form.is_valid():
            menu_order = order_form.save(commit=False)
            menu_order.client = request.user
            menu_order.save()
            return redirect('checkout')
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


def checkout(request):
    context = {
        'client_id': getattr(settings, "PAYPAL_CLIENT_ID", None)
    }
    return render(request, 'checkout.html', context)

