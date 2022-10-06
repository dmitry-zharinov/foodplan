from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import MenuForm

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
    context = {
    }
    return render(request, 'menu.html', context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})
