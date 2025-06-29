from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.urls import reverse

# Importação correta dos formulários
from  coverde_ecommerce.forms import LoginForm, ProdutorRegistrationForm, ConsumidorRegistrationForm

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
            messages.success(request, f'Bem-vindo(a), {user.first_name}!')
            return redirect(self.get_redirect_url(user))
        messages.error(request, 'E-mail ou senha inválidos. Tente novamente.')
        return render(request, self.template_name, {'form': form})

    def get_redirect_url(self, user):
        if user.tipo == 'P':
            return reverse('coverde_ecommerce:produtor_dashboard')
        elif user.tipo == 'C':
            return reverse('coverde_ecommerce:consumidor_dashboard')
        return reverse('coverde_ecommerce:index')

def custom_logout(request):
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('coverde_ecommerce:index')

def registration_choice(request):
    if request.user.is_authenticated:
        return redirect('coverde_ecommerce:index')
    return render(request, 'coverde_ecommerce/auth/registration_choice.html')

def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect('coverde_ecommerce:produtor_dashboard')
    
    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de produtor criada com sucesso!')
            return redirect('coverde_ecommerce:produtor_dashboard')
    else:
        form = ProdutorRegistrationForm()
    
    return render(request, 'coverde_ecommerce/auth/signup_produtor.html', {'form': form})

def signup_consumidor(request):
    if request.user.is_authenticated:
        return redirect('coverde_ecommerce:consumidor_dashboard')
    
    if request.method == 'POST':
        form = ConsumidorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de consumidor criada com sucesso!')
            return redirect('coverde_ecommerce:consumidor_dashboard')
    else:
        form = ConsumidorRegistrationForm()
    
    return render(request, 'coverde_ecommerce/auth/signup_consumidor.html', {'form': form})