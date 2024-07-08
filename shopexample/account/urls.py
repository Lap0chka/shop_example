from django.shortcuts import render
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # Registration and verification
    path('register/', views.register, name='register'),
    path('email-verification-sent/',
         lambda request: render(request, 'account/email/email-verification-sent.html'),
         name='email_verification_sent'
         ),
    # Login and Logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_user, name='profile_user'),
    path('delete-account/', views.delete_account, name='profile_delete')
]
