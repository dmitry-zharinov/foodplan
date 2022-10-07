from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import json
from .forms import MenuForm
from .models import Menu, Recipe


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['menu'] = Menu.objects.filter(client=request.user).first()
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
    context = {}
    if request.method == "POST":
        order_form = MenuForm(request.POST)
        if order_form.is_valid():
            menu_order = order_form.save(commit=False)
            menu_order.client = request.user
            #menu_order.save()
            request.session['_menu_order'] = request.POST
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


def payment_complete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    new_menu = Menu.objects.create(
        client=request.user,
        period=body['period'],
        calories_per_day=body['calories_per_day'],
        with_breakfasts=True if body['with_breakfasts'] == "on" else False,
        with_lunches=True if body['with_lunches'] == "on" else False,
        with_suppers=True if body['with_suppers'] == "on" else False,
        with_desserts=True if body['with_desserts'] == "on" else False,
        persons=body['persons'],
    )
    for allergen in body['allergens']:
        new_menu.allergens.set(allergen)
    #new_menu.allergens.set(body['allergens'])
    return redirect('index')


@login_required
def checkout(request):
    menu_order = request.session.get('_menu_order')
    context = {
        'client_id': getattr(settings, "PAYPAL_CLIENT_ID", None),
        'menu_order': menu_order,
    }
    context['current_menu'] = Menu.objects.filter(client=request.user).first()
    return render(request, 'checkout.html', context)
