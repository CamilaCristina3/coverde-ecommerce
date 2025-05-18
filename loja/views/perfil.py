from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ConfiguracoesContaView(LoginRequiredMixin, TemplateView):
    template_name = 'pt/perfil/configuracoes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione lógica adicional se necessário
        return context