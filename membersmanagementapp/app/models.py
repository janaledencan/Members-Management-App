from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import datetime
from datetime import date


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.CharField(max_length=20)
    address = models.CharField(max_length=25)
    country = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_owner_profile(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_owner_profile(sender, instance, **kwargs):
    instance.owner.save()


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=300, default=None)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.owner.user.username}"

    def save(self, *args, **kwargs):
        if not self.owner_id:
            self.owner = get_user_model().objects.get(pk=kwargs["request"].user.pk)
        super().save(*args, **kwargs)

    @classmethod
    def get_all_groups(self):
        return Group.objects.all()

    @classmethod
    def get_group_by_id(self, id):  # provjeri
        return Group.objects.get(pk=id)


class Gender(models.TextChoices):
    male = "M"
    female = "F"


class Member(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # get_user_model()
    name = models.CharField(blank=False, max_length=40)
    surname = models.CharField(blank=False, max_length=50)
    date_of_birth = models.DateField(default=datetime.date.today)  # ovo
    # formatted_str = date_obj.strftime('%Y-%m-%d')
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.male,
    )

    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateField(default=datetime.date.today)
    # prikaz u oblacicu  - bilo je datetime.date.today

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"

    def save(self, *args, **kwargs):
        if not self.owner_id:
            self.owner = get_user_model().objects.get(kwargs["request"].user)
        super().save(*args, **kwargs)

    @classmethod
    def get_all_members(self):
        return Member.objects.all()

    @classmethod
    def get_member_by_id(self, id):  # provjeri
        return Member.objects.get(pk=id)


class MembersInGroup(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.member.name} - {self.group.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
