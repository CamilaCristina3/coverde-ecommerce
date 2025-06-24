from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from ..forms import ResendVerificationForm
import uuid

User = get_user_model()

class ResendVerificationView(FormView):
    template_name = 'coverde_ecommerce/auth/resend_verification.html'
    form_class = ResendVerificationForm
    success_url = reverse_lazy('coverde_ecommerce:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            
            if user.email_verified:
                messages.warning(self.request, "Este e-mail já está verificado.")
                return super().form_valid(form)
            
            # Gerar novo token (exemplo simplificado)
            new_token = uuid.uuid4().hex
            
            # Atualizar token do usuário (ajuste conforme seu modelo)
            user.verification_token = new_token
            user.save()
            
            # Enviar e-mail (exemplo simplificado)
            verification_url = self.request.build_absolute_uri(
                reverse('coverde_ecommerce:verificar_email') + f'?token={new_token}&uid={user.id}'
            )
            
            send_mail(
                'Confirmação de E-mail - COVERDE',
                f'Clique no link para verificar seu e-mail: {verification_url}',
                'noreply@coverde.com.br',
                [email],
                fail_silently=False,
            )
            
            messages.success(self.request, "Novo link de verificação enviado com sucesso!")
        except User.DoesNotExist:
            messages.error(self.request, "E-mail não encontrado em nosso sistema.")
        
        return super().form_valid(form)