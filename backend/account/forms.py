from typing import Any

from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django_email_verification import send_email


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already used")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()
            send_email(user)

        return user





class UserUpdateForm(forms.ModelForm):
    new_email = forms.EmailField(required=False)
    password = forms.CharField(label='Current password', widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # email только для отображения

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower()
        new_email = cleaned_data.get('new_email', '').lower()

        if new_email:
            if email == new_email:
                raise ValidationError("New email and current email are the same.")

            if User.objects.filter(email=new_email).exists():
                raise ValidationError("Email is already in use.")

        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("New passwords do not match.")

            if not password:
                raise ValidationError("Current password is required to change password.")

            if not self.instance.check_password(password):
                raise ValidationError("Current password is incorrect.")

        return cleaned_data

    def save(self, commit=True, user=None):
        user = user or self.instance  # fallback на self.instance

        new_email = self.cleaned_data.get('new_email')
        if new_email:
            user.email = new_email
            user.is_active = False
            send_email(user)

        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)

        if commit:
            user.save()

        return user