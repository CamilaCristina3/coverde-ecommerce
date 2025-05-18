# loja/views/auth/verificacao_email.py

from django.views.generic import TemplateView

class SignupEmailVerificationView(TemplateView):
    """Vista de confirmação/verificação de e-mail após registo"""
    template_name = 'pt/auth/verificacao_email.html'
