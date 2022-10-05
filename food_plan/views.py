from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Recipe


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


@login_required
def profile(request):
    context = {
    }
    return render(request, 'lk.html', context)


def order(request):
    context = {
    }
    return render(request, 'order.html', context)


def menu(request):
    context = {
    }
    return render(request, 'menu.html', context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})
