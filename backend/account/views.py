from django.contrib import messages
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from typing import Type
from account.forms import UserUpdateForm, CustomUserCreationForm
from django.contrib.auth.base_user import AbstractBaseUser


User: Type[AbstractBaseUser] = get_user_model()

class UserRegisterView(CreateView):
    template_name = 'account/registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account:email_verification_sent')


class CustomLoginView(LoginView):
    template_name = 'account/login/login.html'
    redirect_authenticated_user = True


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard/dashboard.html'


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'account/dashboard/profile_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('account:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.save(user=self.request.user)
        messages.success(
            self.request,
            'Your account has been updated! You need to confirm your new email address'
        )
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account/dashboard/confirm_delete.html'
    success_url = reverse_lazy('account:login')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your account has been deleted.')
        logout(request)
        return super().delete(request, *args, **kwargs)
