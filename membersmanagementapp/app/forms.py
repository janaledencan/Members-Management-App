from django.forms import ModelForm
from django import forms
from .models import Owner, Member, Group
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import datetime
from django.db.models import Q


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]


class SetEmailForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["email"]


class EmailChangeForm(forms.Form):
    error_messages = {
        "email_mismatch": ("The two email addresses fields didn't match."),
        "not_changed": ("The email address is the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get("new_email1")
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages["not_changed"],
                    code="not_changed",
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get("new_email1")
        new_email2 = self.cleaned_data.get("new_email2")
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages["email_mismatch"],
                    code="email_mismatch",
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class DateInput(forms.DateInput):
    input_type = "date"


class MemberForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput)

    class Meta:
        model = Member
        fields = [
            "name",
            "surname",
            "date_of_birth",
            "gender",
            "email",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control w-75"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        exclude = ("owner", "date_joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["date_of_birth"] = self.instance.date_of_birth

    def clean(self):
        errors = []

        if "name" in self.cleaned_data:
            if self.cleaned_data["name"] == "":
                raise ValidationError("You have to enter a name! ")
            elif not self.cleaned_data["name"][0].isupper():
                raise ValidationError(
                    "You must enter the name with the first letter capitalized!"
                )

        if "surname" in self.cleaned_data:
            if self.cleaned_data["surname"] == "":
                raise ValidationError("You have to enter surname! ")
            elif not self.cleaned_data["surname"][0].isupper():
                raise ValidationError(
                    "You must enter the surname with the first letter capitalized!"
                )

        if "date_of_birth" in self.cleaned_data:
            if self.cleaned_data["date_of_birth"] > datetime.date.today():
                errors.append(
                    ValidationError("The date of birth cannot be in the future! ")
                )
        else:
            errors.append(ValidationError("Date of birth field is empty. "))

        if errors:
            raise ValidationError(errors)
        return self.cleaned_data


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control "}),
        }
        exclude = ("owner",)

    def clean(self):
        errors = []

        if "price" in self.cleaned_data:
            if self.cleaned_data["price"] < 0:
                errors.append(ValidationError("The price cannot be less than 0! "))
        else:
            errors.append(ValidationError("Price field empty. "))

        if "description" in self.cleaned_data:
            if self.cleaned_data["description"] == "":
                raise ValidationError("You have to enter a description! ")

        if errors:
            raise ValidationError(errors)
        return self.cleaned_data


class SearchForm(forms.Form):
    search_query = forms.CharField(required=False)
    filter_choice = forms.ChoiceField(
        choices=[
            ("name", "Name"),
            ("surname", "Surname"),
            ("email", "Email"),
            ("gender", "Gender (M/F)"),
            ("date_joined", "Date of joining"),
        ],
        widget=forms.RadioSelect,
        required=False,
    )

    sort_choice = forms.ChoiceField(
        choices=[
            ("asc", "Ascending"),
            ("desc", "Descending"),
        ],
        widget=forms.RadioSelect,
        required=False,
    )
