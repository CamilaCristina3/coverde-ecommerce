from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

class SobreView(TemplateView):
    template_name = 'pt/institucional/sobre.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = _("Sobre Nós")
        return context

class ContactosView(TemplateView):
    template_name = 'pt/institucional/contactos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = _("Contactos")
        return context

class PoliticaPrivacidadeView(TemplateView):
    template_name = 'pt/institucional/privacidade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = _("Política de Privacidade")
        return context

class ComoFuncionaView(TemplateView):
    template_name = 'pt/institucional/como_funciona.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = _("Como Funciona")
        return context