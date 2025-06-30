from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from coverde_ecommerce.forms import LoginForm

class LoginView(View):
    template_name = 'coverde_ecommerce/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url(request.user))
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Define backend explicitamente se múltiplos forem usados
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, f'Bem-vindo(a), {user.first_name}!')
            return redirect(self.get_redirect_url(user))

        messages.error(request, 'E-mail ou senha inválidos. Tente novamente.')
        return render(request, self.template_name, {'form': form})

    def get_redirect_url(self, user):
        if user.tipo == 'P':  # Produtor
            return reverse('coverde_ecommerce:dashboard_produtor')
        elif user.tipo == 'C':  # Consumidor
            return reverse('coverde_ecommerce:produto_list')
        return reverse('coverde_ecommerce:index')
