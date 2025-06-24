from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from coverde_ecommerce.views.auth import get_dashboard_redirect
from coverde_ecommerce.forms import (
    ProdutorRegistrationForm, ConsumidorRegistrationForm
)

def registration_choice(request):
    return render(request, 'coverde_ecommerce/auth/registration_choice.html')

def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))
    
    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de produtor criada!')
            return redirect('coverde_ecommerce:produtor_dashboard')
    else:
        form = ProdutorRegistrationForm()
    
    return render(request, 'coverde_ecommerce/auth/signup_produtor.html', {'form': form})

def signup_consumidor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))
    
    if request.method == 'POST':
        form = ConsumidorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de consumidor criada!')
            return redirect('coverde_ecommerce:listagem-produto')
    else:
        form = ConsumidorRegistrationForm()
    
    return render(request, 'coverde_ecommerce/auth/signup_consumidor.html', {'form': form})