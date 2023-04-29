from django.forms import ModelForm
from django import forms
from .models import Owner, Member, Group
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms


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
        fields = ["name", "surname", "date_of_birth", "gender", "email"]
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):  # Trenutno nije nužno
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["date_of_birth"] = self.instance.date_of_birth


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ("owner",)
