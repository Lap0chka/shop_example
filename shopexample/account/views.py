from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django_email_verification import send_email

from account.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create(username=username, email=email, password=password, is_active=False)
            send_email(user)

            return redirect('/account/email-verification-sent/')
    else:
        form = UserRegisterForm()
    return render(request, 'account/registration/register.html', {'form': form})
