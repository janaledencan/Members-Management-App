from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, OwnerRegistrationForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from app.forms import SetPasswordForm, EmailChangeForm, SetEmailForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        owner_registration_form = OwnerRegistrationForm(request.POST)
        if registration_form.is_valid() and owner_registration_form.is_valid():
            user = registration_form.save()
            user.refresh_from_db()
            owner_registration_form = OwnerRegistrationForm(
                request.POST, instance=user.owner
            )
            owner_registration_form.full_clean()
            owner_registration_form.save()

            messages.success(request, "Registration successful.")
            return redirect("login")
        else:
            context = {
                "registration_form": registration_form,
                "owner_registration_form": owner_registration_form,
            }
    else:
        registration_form = UserRegistrationForm()
        owner_registration_form = OwnerRegistrationForm()
        context = {
            "registration_form": registration_form,
            "owner_registration_form": owner_registration_form,
        }
    return render(
        request=request,
        template_name="registration/registration.html",
        context=context,
    )


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
    return render(request, "accounts/profile.html", context)


@login_required()
def change_email(request, user_id):
    user = request.user
    form = EmailChangeForm(user)

    if request.method == "POST":
        form = EmailChangeForm(user, request.POST)
        password_form = SetPasswordForm(user)

        if form.is_valid():
            form.save()
            context = {
                "user": user,
                "email_form": form,
                "password_form": password_form,
            }

        return HttpResponseRedirect(reverse("accounts:profile", args=[user_id]))
    else:
        context = {"user": user, "email_form": form, "password_form": password_form}
        return render(request, "accounts/profile.html", context)


@login_required()
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
        return HttpResponseRedirect(request, "accounts/profile.html", context)
    else:
        form = SetPasswordForm(user)
        context = {"user": user, "form": form}
        return render(request, "accounts/profile.html", context)
