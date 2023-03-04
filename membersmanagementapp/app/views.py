from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MemberForm
from .models import Member
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    context = {}
    return render(request, "app/home.html", context)


def management(request):
    user = request.user
    members = Member.get_all_members()
    context = {"user": user, "members": members}
    return render(request, "app/management.html", context)


def members(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = Member.objects.create(
                owner=request.user,
                name=form.cleaned_data.get("name"),
                surname=form.cleaned_data.get("surname"),
                date=form.cleaned_data.get("date_of_birth"),
                gender=form.cleaned_data.get("gender"),
                email=form.cleaned_data.get("email"),
            )
            member.save()
            return HttpResponseRedirect(reverse("app:management", args=[]))
        else:
            context = {"form": form}
            return render(request, "management/add_member.html", context)
    else:
        form = MemberForm()
    return render(request, "management/add_member.html", {"form": form})


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
