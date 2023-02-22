from django.urls import path
from . import views
from django.urls import include
from .forms import SetEmailForm, EmailChangeForm


app_name = "app"
urlpatterns = [
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/password_change", views.change_password, name="new_password"),
    path("profile/email_change", views.change_email, name="new_email"),
]
