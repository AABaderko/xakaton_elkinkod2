from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import (
    AppUser, MessageChat
)

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    password = ReadOnlyPasswordHashField(label=("Password"))

    class Meta:
        model = AppUser
        fields = ('username', 'tg_id', 'first_name', 'last_name', 'timezone', 'workgroup', 'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        #AppUser.set_password(user, self.cleaned_data["password1"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user