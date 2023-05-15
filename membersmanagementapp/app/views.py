from django.shortcuts import render, redirect
from .forms import MemberForm, GroupForm
from .models import Member, Group, MembersInGroup
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic.edit import CreateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    context = {}
    return render(request, "app/home.html", context)


@login_required()
def management(request):
    user = request.user
    members = Member.get_all_members()
    groups = Group.get_all_groups
    members_in_group = MembersInGroup.get_all_members_in_group()
    context = {
        "user": user,
        "members": members,
        "groups": groups,
        "members_in_group": members_in_group,
    }
    return render(request, "app/management.html", context)


@login_required()
def members(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = Member.objects.create(
                owner=request.user,
                name=form.cleaned_data.get("name"),
                surname=form.cleaned_data.get("surname"),
                date_of_birth=form.cleaned_data.get("date_of_birth"),
                gender=form.cleaned_data.get("gender"),
                email=form.cleaned_data.get("email"),
            ).save()

            return HttpResponseRedirect(reverse("app:management", args=[]))
        else:
            context = {"form": form}
            print(form.errors)
            return render(request, "management/add_member.html", context)
    else:
        form = MemberForm()
    return render(request, "management/add_member.html", {"form": form})


@login_required()
def edit(request, id):
    member = Member.get_member_by_id(id)
    return render(request, "management/edit.html", {"member": member})


@login_required()
def update(request, id):
    member = Member.get_member_by_id(id)
    form = MemberForm(request.POST, instance=member)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("app:management", args=[]))

    return render(request, "management/edit.html", {"member": member, "form": form})


@login_required()
def destroy(request, id):
    member = Member.get_member_by_id(id)
    member.delete()
    return HttpResponseRedirect(reverse("app:management", args=[]))


@login_required()
def groups(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = Group.objects.create(
                owner=request.user,
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                price=form.cleaned_data.get("price"),
            ).save()

            return HttpResponseRedirect(reverse("app:management", args=[]))
        else:
            context = {"form": form}
            return render(request, "management/add_new_group.html", context)
    else:
        form = GroupForm()
    return render(request, "management/add_new_group.html", {"form": form})


@login_required()
def edit_group(request, id):
    group = Group.get_group_by_id(id)
    return render(request, "management/edit_group.html", {"group": group})


@login_required()
def update_group(request, id):
    group = Group.get_group_by_id(id)
    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("app:management", args=[]))

    return render(request, "management/edit_group.html", {"group": group, "form": form})


@login_required()
def destroy_group(request, id):
    group = Group.get_group_by_id(id)
    group.delete()
    return HttpResponseRedirect(reverse("app:management", args=[]))


@login_required()
def group_details(request, group_id):
    user = request.user
    group = Group.objects.get(pk=group_id)

    members_in_group = MembersInGroup.objects.all().filter(Q(group=group))
    other_members = Member.objects.all()

    members_not_in_group = other_members.exclude(
        id__in=members_in_group.values("member__id")
    )
    context = {
        "user": user,
        "group": group,
        "members_in_group": members_in_group,
        "members_not_in_group": members_not_in_group,
    }

    if request.method == "POST":
        id_members = request.POST.getlist("boxes")

        members_in_group.update(is_paid=False)

        for x in id_members:
            members_in_group.filter(pk=int(x)).update(is_paid=True)

        messages.success(request, ("Update paid"))
        return HttpResponseRedirect(reverse("app:group_details", args=[group.id]))

    return render(request, "app/group_details.html", context)


@login_required()
def view_member(request, id):
    return HttpResponseRedirect(reverse("app:management"))


@login_required()
def add_member_to_group(request, group_id, member_id):
    member = Member.objects.get(pk=member_id)
    group = Group.objects.get(pk=group_id)

    MembersInGroup.objects.create(
        member=member,
        group=group,
    ).save()

    return HttpResponseRedirect(reverse("app:group_details", args=[group.id]))


@login_required()
def remove_member_from_group(request, group_id, member_id):
    member = Member.objects.get(pk=member_id)
    group = Group.objects.get(pk=group_id)

    MembersInGroup.objects.filter(Q(member=member), Q(group=group)).delete()

    return HttpResponseRedirect(reverse("app:group_details", args=[group.id]))


@login_required()
def admin_approval(request, group_id, member_id):
    return render(request, "app:group_details.html")
