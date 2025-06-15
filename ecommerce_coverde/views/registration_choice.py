from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ecommerce_coverde.views.auth import get_dashboard_redirect
from ecommerce_coverde.forms import (
    ProdutorRegistrationForm, ConsumidorRegistrationForm
)

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