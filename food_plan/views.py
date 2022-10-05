from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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