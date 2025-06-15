from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import View
from django.contrib import messages
from ecommerce_coverde.forms import LoginForm

class LoginView(View):
    template_name = 'ecommerce_coverde/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url(request.user))
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_short_name()}!')
            return redirect(self.get_redirect_url(user))
        messages.error(request, 'E-mail ou senha inválidos. Tente novamente.')
        return render(request, self.template_name, {'form': form})

    def get_redirect_url(self, user):
        if user.tipo == 'P':
            return reverse('ecommerce_coverde:produtor_dashboard')
        elif user.tipo == 'C':
            return reverse('ecommerce_coverde:consumidor_dashboard')
        return reverse('ecommerce_coverde:index')