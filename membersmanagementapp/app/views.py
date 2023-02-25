from django.shortcuts import render
from django.contrib.auth import login


def home(request):
    context = {}
    return render(request, "app/home.html", context)
