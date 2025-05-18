from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class LoginView(View):  # ← Aqui está a definição da classe que você quer importar
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('loja:index')
        return render(request, 'pt/auth/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, _('Login efetuado com sucesso!'))
            
            if user.tipo == 'P':  # Produtor
                return redirect('loja:dashboard')
            return redirect('loja:index')
        
        messages.error(request, _('Credenciais inválidas'))
        return render(request, 'pt/auth/login.html')