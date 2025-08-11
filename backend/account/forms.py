from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from account.services import update_user_email, change_user_password
from account.validators import validate_email_available, validate_password_change


class UserRegisterForm(UserCreationForm):
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

        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        validate_password_change(
            user=self.instance,
            current_password=cleaned_data.get('password'),
            new_password1=cleaned_data.get('password1'),
            new_password2=cleaned_data.get('password2'),
        )

        return cleaned_data

    def save(self, commit=True, user=None):
        user = user or self.instance
        user = update_user_email(user, self.cleaned_data.get('new_email'))
        user = change_user_password(user, self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user