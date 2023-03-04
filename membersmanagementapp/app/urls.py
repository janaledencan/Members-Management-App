from django.urls import path
from . import views
from django.urls import include


app_name = "app"
urlpatterns = [
    path("management/", views.management, name="management"),
    path("management/member", views.members, name="add_member"),
    path("management/edit/<int:id>", views.edit, name="edit_member"),
    path("management/update/<int:id>", views.update, name="update_member"),
    path("management/delete/<int:id>", views.destroy, name="delete_member"),
]
