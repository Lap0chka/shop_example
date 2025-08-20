from typing import  Type

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from account.services import change_user_password, update_user_email
from account.validators import (
    validate_email_available,
    validate_email_is_the_same,
    validate_password_change,
)
from django.contrib.auth.base_user import AbstractBaseUser


User: Type[AbstractBaseUser] = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_available])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        return update_user_email(user, self.cleaned_data['email'])



class UserUpdateForm(forms.ModelForm):
    new_email = forms.EmailField(required=False, validators=[validate_email_available])
    password = forms.CharField(label='Current password', widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        old_email, new_email = (
            cleaned_data.get('email'),
            cleaned_data.get('new_email'),
        )
        password, password1, password2 = (
            cleaned_data.get('password'),
            cleaned_data.get('password1'),
            cleaned_data.get('password2'),
        )

        validate_password_change(
            user=self.instance,
            current_password=password,
            new_password1=password1,
            new_password2=password2,
        )
        validate_email_is_the_same(old_email=old_email, new_email=new_email)
        return cleaned_data

    def save(self, commit=True, user=None):
        user = user or self.instance
        user = update_user_email(user)
        user = change_user_password(user, self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user
