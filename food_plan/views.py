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
    BASE_PRICE = 100
    context = {}
    if request.method == "POST":
        order_form = MenuForm(request.POST)
        if order_form.is_valid():
            menu_order = order_form.save(commit=False)
            menu_order.client = request.user
            #menu_order.save()
            request.session['_menu_order'] = request.POST
            request.session['_price'] = BASE_PRICE * int(menu_order.period)
            return redirect('checkout')
        else:
            print(order_form.errors.as_data())
    else:
        order_form = MenuForm()
        context = {
            'order_form': order_form,
            'base_price': BASE_PRICE
        }
    return render(request, 'order.html', context)


@login_required
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
    current_menu = Menu.objects.get(client=request.user)
    breakfast_calories = current_menu.calories_per_day * 0.2
    lunch_calories = current_menu.calories_per_day * 0.3
    supper_calories = current_menu.calories_per_day * 0.3
    dessert_calories = current_menu.calories_per_day * 0.2
    if current_menu.with_breakfasts:
        breakfasts = Recipe.objects.filter(
            type='breakfast',
            calories__lte=breakfast_calories
        )[:7]
    else:
        breakfasts = None
    if current_menu.with_lunches:
        lunches = Recipe.objects.filter(
            type='lunch',
            calories__lte=lunch_calories
        )[:7]
    else:
        lunches = None
    if current_menu.with_suppers:
        suppers = Recipe.objects.filter(
            type='supper',
            calories__lte=supper_calories
        )[:7]
    else:
        suppers = None
    if current_menu.with_desserts:
        desserts = Recipe.objects.filter(
            type='dessert',
            calories__lte=dessert_calories
        )[:7]
    else:
        desserts = None
    week_menu = {}
    limitless_breakfasts = get_meal_for_day(breakfasts)
    limitless_lunches = get_meal_for_day(lunches)
    limitless_suppers = get_meal_for_day(suppers)
    limitless_desserts = get_meal_for_day(desserts)
    for day in days:
        week_menu[day] = [
            next(limitless_breakfasts) if breakfasts else None,
            next(limitless_lunches) if lunches else None,
            next(limitless_suppers) if suppers else None,
            next(limitless_desserts) if desserts else None,
        ]
    context = {
        'client': current_menu.client,
        'week': days,
        'menu': week_menu,
    }
    return render(request, 'menu.html', context)


def get_meal_for_day(meal):
    day_number = 0
    while day_number < 7:
        if day_number >= meal.count():
            day_number = 0
        yield meal[day_number]
        day_number += 1


@login_required
def recipe(request, recipe_id):
    current_menu = Menu.objects.get(client=request.user)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    serialized_ingredients = {}
    for ingredient in recipe.ingredients.all():
        serialized_ingredients[ingredient.title] = {
            'amount': round(
                ingredient.amount / recipe.portions * current_menu.persons, 1
            ),
            'unit': ingredient.unit,
            'price': ingredient.price,
            'allergen': ingredient.allergen,
        }
    context = {
        'recipe': recipe,
        'persons': current_menu.persons,
        'ingredients': serialized_ingredients,
    }
    return render(request, 'recipe.html', context)


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
    price = request.session.get('_price')
    context = {
        'client_id': getattr(settings, "PAYPAL_CLIENT_ID", None),
        'price': price,
        'menu_order': menu_order,
    }
    context['current_menu'] = Menu.objects.filter(client=request.user).first()
    return render(request, 'checkout.html', context)
