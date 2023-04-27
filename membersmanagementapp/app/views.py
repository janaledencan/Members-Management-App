from django.shortcuts import render, redirect
from .forms import MemberForm, GroupForm
from .models import Member, Group
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic.edit import CreateView


def home(request):
    context = {}
    return render(request, "app/home.html", context)


def management(request):
    user = request.user
    members = Member.get_all_members()
    groups = Group.get_all_groups
    context = {"user": user, "members": members, "groups": groups}
    return render(request, "app/management.html", context)


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = "management/add_member.html"


def edit(request, id):
    member = Member.get_member_by_id(id)
    return render(request, "management/edit.html", {"member": member})


def update(request, id):
    member = Member.get_member_by_id(id)
    form = MemberForm(request.POST, instance=member)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("app:management", args=[]))

    return render(request, "management/edit.html", {"member": member})


def destroy(request, id):
    member = Member.get_member_by_id(id)
    member.delete()
    return HttpResponseRedirect(reverse("app:management", args=[]))


def groups(request):
    if request.method == "POST":
        form = GroupForm(request.POST, owner=request.user)
        if form.is_valid():
            group = Group.objects.create(
                owner=request.user.owner,
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                price=form.cleaned_data.get("price"),
            )
            group.save()
            return HttpResponseRedirect(reverse("app:management", args=[]))
        else:
            context = {"form": form}
            return render(request, "management/add_new_group.html", context)
    else:
        form = GroupForm()
    return render(request, "management/add_new_group.html", {"form": form})


def edit_group(request, id):
    group = Group.get_group_by_id(id)
    return render(request, "management/edit_group.html", {"group": group})


def update_group(request, id):
    group = Group.get_group_by_id(id)
    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("app:management", args=[]))

    return render(request, "management/edit_group.html", {"group": group})


def destroy_group(request, id):
    group = Group.get_group_by_id(id)
    group.delete()
    return HttpResponseRedirect(reverse("app:management", args=[]))
