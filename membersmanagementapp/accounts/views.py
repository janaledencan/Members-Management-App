from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, OwnerRegistrationForm
from django.contrib.auth import login
from django.contrib import messages

from django.urls import reverse_lazy
from django.views import generic

# Create your views here.


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
