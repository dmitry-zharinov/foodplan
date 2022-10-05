from django.shortcuts import render


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


def profile(request):
    context = {
    }
    return render(request, 'lk.html', context)


def order(request):
    context = {
    }
    return render(request, 'order.html', context)