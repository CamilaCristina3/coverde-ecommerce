from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

class IndexView(TemplateView):
    """View para a página inicial"""
    template_name = 'pt/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = _("Bem-vindo à COVERDE")
        # Adicione outros contextos necessários
        return context

class LojaView(TemplateView):
    """View para a página da loja"""
    template_name = 'pt/loja.html'