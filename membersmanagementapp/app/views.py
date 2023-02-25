from django.shortcuts import render
from django.contrib.auth import login


def home(request):
    context = {}
    return render(request, "app/home.html", context)


def management(request):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "app/management.html", context)
