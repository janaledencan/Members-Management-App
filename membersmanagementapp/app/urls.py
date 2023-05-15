from django.urls import path
from . import views
from django.urls import include

app_name = "app"
urlpatterns = [
    path("management/", views.management, name="management"),
    path("management/member/", views.members, name="add_member"),
    path("management/member/<int:id>", views.view_member, name="view_member"),
    path("management/edit/<int:id>", views.edit, name="edit_member"),
    path("management/update/<int:id>", views.update, name="update_member"),
    path("management/delete/<int:id>", views.destroy, name="delete_member"),
    # novi
    path("management/group", views.groups, name="add_group"),
    path("management/edit-group/<int:id>", views.edit_group, name="edit_group"),
    path("management/update-group/<int:id>", views.update_group, name="update_group"),
    path("management/delete-group/<int:id>", views.destroy_group, name="delete_group"),
    # za grupe
    path(
        "management/group/<int:group_id>/add_member/<int:member_id>",
        views.add_member_to_group,
        name="add_member_to_group",
    ),
    path(
        "management/group/<int:group_id>/remove_member/<int:member_id>",
        views.remove_member_from_group,
        name="remove_member_from_group",
    ),
    path("management/group/<int:group_id>", views.group_details, name="group_details"),
    path(
        "management/group/<int:group_id>/admin_approval",
        views.admin_approval,
        name="admin_approval",
    ),
]
