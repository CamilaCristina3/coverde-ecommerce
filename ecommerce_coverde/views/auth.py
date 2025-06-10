from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from ecommerce_coverde.forms import ProdutorRegistrationForm, ConsumidorRegistrationForm
from ecommerce_coverde.models import Utilizador


def login_view(request):
    if request.user.is_authenticated:
        return redirect('ecommerce_coverde:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_short_name()}!')
            return redirect(get_dashboard_redirect(user))
        messages.error(request, 'Credenciais inválidas')
    else:
        form = AuthenticationForm()
    
    return render(request, 'ecommerce_coverde/auth/login.html', {'form': form})

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Você foi desconectado')
    return redirect('ecommerce_coverde:index')

def registration_choice(request):
    return render(request, 'ecommerce_coverde/auth/registration_choice.html')

def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))
    
    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de produtor criada!')
            return redirect('ecommerce_coverde:produtor_dashboard')
    else:
        form = ProdutorRegistrationForm()
    
    return render(request, 'ecommerce_coverde/auth/signup_produtor.html', {'form': form})

def signup_consumidor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))
    
    if request.method == 'POST':
        form = ConsumidorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de consumidor criada!')
            return redirect('ecommerce_coverde:listagem-produto')
    else:
        form = ConsumidorRegistrationForm()
    
    return render(request, 'ecommerce_coverde/auth/signup_consumidor.html', {'form': form})

def get_dashboard_redirect(user):
    if user.tipo == 'P':
        return 'ecommerce_coverde:produtor_dashboard'
    elif user.tipo == 'C':
        return 'ecommerce_coverde:consumidor_dashboard'
    return 'ecommerce_coverde:index'