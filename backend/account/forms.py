from typing import Any

from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django_email_verification import send_email


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = False
        self.fields['password1'].help_text = False
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already used")
        return email


class UserUpdateForm(forms.ModelForm):
    new_email = forms.EmailField(required=False)
    password = forms.CharField(label='Old password', widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', ]
        read_only_fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data['email'].lower()
        new_email = cleaned_data['new_email'].lower()

        if email == new_email:
            raise forms.ValidationError("New email and old are the same")

        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("Email is already used")

        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        user = User.objects.get(email=email)

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("New passwords do not match.")

        if password and user.check_password(password):
            raise forms.ValidationError("Current password is incorrect.")

        return cleaned_data

    def save(self, commit=True, user=None):

        email = self.cleaned_data.get('new_email')
        if email:
            user.email = email
            user.is_active = False
            send_email(user)

        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)

        if commit:
            user.save()

        return user
