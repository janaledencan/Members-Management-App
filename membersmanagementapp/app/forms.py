from django.forms import ModelForm
from django import forms
from .models import Owner


class UserProfileForm(ModelForm):
    is_translator = forms.BooleanField()

    class Meta:
        model = Owner
        fields = [
            "token_balance",
            "is_translator",
        ]

        widgets = {
            "token_balance": forms.NumberInput(attrs={"class": "form-control"}),
            "is_translator": forms.CheckboxInput(attrs={"class": "form-control"}),
        }


# class UserUpdateForm(forms.ModelForm):
#    email = forms.EmailField()

#   class Meta:
#       model = get_user_model()
#       fields = ['first_name', 'last_name', 'email', 'description']
