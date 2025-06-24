from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model

# Obtém o modelo customizado de Utilizador
Utilizador = get_user_model()

class SignupEmailCheck(View):
    """Verifica a disponibilidade de email durante o registo"""
    
    template_name = "auth/signup_email.html"
    
    def get(self, request):
        """Exibe o formulário de verificação de email"""
        return render(request, self.template_name)
    
    def post(self, request):
        """Processa a verificação do email"""
        email = request.POST.get("email", "").strip()
        
        # Validação básica do email
        if not email or "@" not in email:
            messages.error(request, "Por favor, insira um endereço de email válido.")
            return render(request, self.template_name, {'email': email})
        
        # Verifica se o email já está registado
        if Utilizador.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "Este email já está registado. "
                "Por favor utilize outro ou recupere a sua conta."
            )
            return render(request, self.template_name, {'email': email})
        
        # Armazena o email na sessão para o próximo passo
        request.session["signup_email"] = email
        request.session.modified = True
        
        return redirect("signup_continue")