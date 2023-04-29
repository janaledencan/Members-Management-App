from django.urls import path
from . import views
from django.urls import include

app_name = "app"
urlpatterns = [
    path("management/", views.management, name="management"),
    path("management/member/", views.members, name="add_member"),
    path("management/edit/<int:id>", views.edit, name="edit_member"),
    path("management/update/<int:id>", views.update, name="update_member"),
    path("management/delete/<int:id>", views.destroy, name="delete_member"),
    # novi
    path("management/group", views.groups, name="add_group"),
    path("management/edit-group/<int:id>", views.edit_group, name="edit_group"),
    path("management/update-group/<int:id>", views.update_group, name="update_group"),
    path("management/delete-group/<int:id>", views.destroy_group, name="delete_group"),
]
