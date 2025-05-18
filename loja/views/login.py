from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from loja.models import Utilizador  # Importe seu modelo personalizado

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('loja:index')  # Redireciona se já estiver autenticado

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticação com email (não usa username)
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, _('Login efetuado com sucesso!'))
            
            # Redirecionamento personalizado por tipo de usuário
            if user.tipo == Utilizador.TipoUtilizador.PRODUTOR:
                return redirect('loja:dashboard_produtor')
            return redirect('loja:index')
        else:
            messages.error(request, _('Email ou password incorretos.'))
    
    return render(request, 'pt/auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, _('Sessão terminada com sucesso.'))
    return redirect('loja:index')