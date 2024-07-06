from django.shortcuts import render
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('email-verification-sent/',
         lambda request: render(request, 'account/email/email-verification-sent.html'),
         name='email_verification_sent'
         ),
]
