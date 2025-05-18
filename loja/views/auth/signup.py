from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Obtém o modelo de usuário personalizado
User = get_user_model()

class SignupConsumidorView(View):
    template_name = 'pt/auth/signup_consumidor.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            user = User.objects.create_user(
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                tipo='C',  # Tipo Consumidor
                telefone=request.POST.get('telefone'),
                nif=request.POST.get('nif'),
                morada=request.POST.get('morada'),
                codigo_postal=request.POST.get('codigo_postal'),
                localidade=request.POST.get('localidade')
            )
            messages.success(request, _('Registo efetuado com sucesso!'))
            return redirect('loja:login')
        
        except Exception as e:
            messages.error(request, _('Erro no registo: ') + str(e))
            return render(request, self.template_name, {
                'form_data': request.POST
            })

class SignupProdutorView(View):
    template_name = 'pt/auth/signup_produtor.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            user = User.objects.create_user(
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                tipo='P',  # Tipo Produtor
                telefone=request.POST.get('telefone'),
                nif=request.POST.get('nif'),
                morada=request.POST.get('morada'),
                codigo_postal=request.POST.get('codigo_postal'),
                localidade=request.POST.get('localidade')
            )
            messages.success(request, _('Registo de produtor efetuado com sucesso!'))
            return redirect('loja:login')
        
        except Exception as e:
            messages.error(request, _('Erro no registo: ') + str(e))
            return render(request, self.template_name, {
                'form_data': request.POST
            })

class SignupEmailVerificationView(View):
    template_name = 'pt/auth/email_verification.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Implementação da verificação de email
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, _('Este email já está registado'))
            return render(request, self.template_name)
        
        # Lógica para enviar código de verificação
        messages.success(request, _('Código de verificação enviado para seu email'))
        return redirect('loja:signup_continue')