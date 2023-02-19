from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    context = {}
    return render(request, "app/home.html", context)


@login_required()
def profile(request, user_id):
    user = request.user
    context = {}
    return render(request, "app/profile.html", context)
