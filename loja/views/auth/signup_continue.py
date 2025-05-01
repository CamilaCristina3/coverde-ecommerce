# loja/views/signup_continue.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from loja.models import User
from django.views import View
from django.contrib import messages

class SignupContinue(View):
    def get(self, request):
        # ✅ Garante que o email foi preenchido na etapa anterior
        email = request.session.get('signup_email')
        if not email:
            messages.warning(request, "Por favor, começa o registo pelo e-mail.")
            return redirect('signup_email')
        return render(request, 'signup_continue.html')

    def post(self, request):
        email = request.session.get("signup_email")
        if not email:
            return redirect("signup_email")

         # ✅ Recolher os dados do formulário
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        telemovel = request.POST.get('telemovel')
        perfil = request.POST.get('perfil')
        password = request.POST.get('password')
        consentimento = request.POST.get('consentimento')

        # ✅ Verifica se o utilizador aceitou o consentimento RGPD
        if not consentimento:
            messages.error(request, "É necessário aceitar a política de privacidade.")
            return redirect('signup_continue')

        # ✅ Verifica se já existe conta com o e-mail
        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return redirect('signup_email')

        # ✅ Cria o novo utilizador
        user = User.objects.create_user(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telemovel=telemovel,
            password=password,
            perfil=perfil
        )

        # ✅ Mensagem de sucesso e redirecionamento
        messages.success(request, "Conta criada com sucesso! Já podes iniciar sessão.")
        return redirect('login')
