from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy

from . import views

app_name = 'account'

urlpatterns = [
    # Registration and verification
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('email-verification-sent/',
         lambda request: render(request, 'account/email/email-verification-sent.html'),
         name='email_verification_sent'
         ),
    # Login and Logout
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile_user'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='profile_delete'),
    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password-reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password-reset-done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password-reset-confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password-reset-complete.html'),
         name='password_reset_complete'),
]
