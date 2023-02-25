from django.urls import path
from . import views
from app.forms import SetEmailForm, EmailChangeForm

app_name = "accounts"
urlpatterns = [
    path("sign-up", views.register, name="registration"),
    path("login", views.login, name="login"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/password_change", views.change_password, name="new_password"),
    path("profile/<int:user_id>/email_change", views.change_email, name="new_email"),
]
