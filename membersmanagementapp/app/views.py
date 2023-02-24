from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from .models import Owner
from .forms import SetPasswordForm, EmailChangeForm, SetEmailForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


# Create your views here.


def home(request):
    context = {}
    return render(request, "app/home.html", context)


@login_required()
def profile(request, user_id):
    user = request.user
    email_form = EmailChangeForm(user)
    password_form = SetPasswordForm(user)
    context = {
        "user": user,
        "email_form": email_form,
        "password_form": password_form,
    }
    return render(request, "app/profile.html", context)


# od starog projekta changerie
def change_email(request):
    if request.method == "POST":
        user = request.user
        email_form = SetEmailForm(instance=user)
        if email_form.is_valid():
            email_form.save()
            context = {
                "user": user,
                "email_form": email_form,
                "password_form": password_form,
            }
            messages.success(request, "Your email has been changed")
            return HttpResponseRedirect(request, "app/profile.html", context)
    else:
        email_form = SetEmailForm(instance=request.user)
        password_form = SetPasswordForm(request.user)
        context = {
            "user": user,
            "email_form": email_form,
            "password_form": password_form,
        }
    return HttpResponseRedirect(request, "app/profile.html", context)


def change_password(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        context = {"user": user, "form": form}
        return HttpResponseRedirect(request, "app/profile.html", context)
    else:
        form = SetPasswordForm(user)
        context = {"user": user, "form": form}
        return render(request, "app/profile.html", context)
