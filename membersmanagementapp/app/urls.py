from django.urls import path
from . import views


app_name = "app"
urlpatterns = [
    path("profile/<int:user_id>", views.profile, name="profile"),
]
