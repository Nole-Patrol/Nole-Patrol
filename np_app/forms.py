from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class EmailSearchForm(forms.Form):
    email = forms.EmailField(label="Email")

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class VerificationForm(forms.Form):
    token = forms.CharField(label="Verification Token")
