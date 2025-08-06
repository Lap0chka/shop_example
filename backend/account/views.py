from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from account.forms import UserUpdateForm
from .forms import UserRegisterForm


class UserRegisterView(FormView):
    template_name = 'account/registration/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('account:email_verification_sent')


class CustomLoginView(LoginView):
    template_name = 'account/login/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('account:dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('shop:products')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard/dashboard.htm'
    login_url = 'account:login'


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'account/dashboard/profile_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('account:dashboard')
    login_url = 'account:login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save(user=self.request.user)
        messages.success(
            self.request,
            'Your account has been updated! You need to confirm your new email address'
        )
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request, *args, **kwargs):
        request.user.delete()
        return redirect('shop:index')

    def get(self, request, *args, **kwargs):
        return render(request, 'account/dashboard/profile_user.html')
