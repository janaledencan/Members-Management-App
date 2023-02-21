from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import UserManager
from .models import Owner

# Create your views here.


def home(request):
    context = {}
    return render(request, "app/home.html", context)


@login_required()
def profile(request, username):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "app/profile.html", context)


# od starog projekta changerie


# @login_required()
# def email_change(request, user_id):
#     user = request.user
#     form = EmailChangeForm(user)

#     if request.method == "POST":
#         form = EmailChangeForm(user, request.POST)
#         password_form = SetPasswordForm(user)

#         if form.is_valid():
#             form.save()
#             context = {
#                 "user": user,
#                 "email_form": form,
#                 "password_form": password_form,
#             }

#         return HttpResponseRedirect(reverse("app:profile", args=[user_id]))
#     else:
#         context = {"user": user, "email_form": form, "password_form": password_form}
#         return render(request, "app/profile.html", context)


# @login_required()
# def change_password(request, user_id):
#     user = request.user
#     email_form = EmailChangeForm(user)
#     if request.method == "POST":
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your password has been changed")
#             return redirect("login")
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)
#         context = {"user": user, "form": form, "email_form": email_form}
#         return HttpResponseRedirect(reverse("app:profile", args=[user_id]))
#     else:
#         form = SetPasswordForm(user)

#         context = {"user": user, "form": form, "email_form": email_form}
#         return render(request, "app/profile.html", context)
