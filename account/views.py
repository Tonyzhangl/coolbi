# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.validators import validate_email, ValidationError
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "account/login.html"

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password', None)
        if not username or not password:
            return redirect('login')

        if User.objects.filter(username=username).exists():
            auth_user = auth_authenticate(username=username, password=password)
            if auth_user:
                auth_login(self.request, auth_user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context


class LogoutView(TemplateView):
    template_name = "account/login.html"

    def logout(self, request):
        user = request.user
        if user.is_authenticated():
            auth_logout(request)
        return redirect('login')


class RegisterView(TemplateView):
    template_name = "account/register.html"

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        confirm_password = self.request.POST.get('confirm_password')
        if not username or not email or not password or not confirm_password:
            return redirect('register')
        try:
            validate_email(email)
        except ValidationError:
            return redirect('register')
        if password != confirm_password:
            return redirect('register')
        if User.objects.filter(email=email).exists():
            return redirect('register')

        User.objects.create_user(email=email, username=username, password=password)

        auth_user = auth_authenticate(username=username, password=password)
        if auth_user:
            auth_login(self.request, auth_user)
            return redirect('login')
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context