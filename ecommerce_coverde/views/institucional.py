from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """View para a página inicial"""
    template_name = 'ecommerce_coverde/institucional/index.html'

def sobre(request):
    return render(request, 'ecommerce_coverde/institucional/sobre.html')

def solucoes(request):
    return render(request, 'ecommerce_coverde/institucional/solucoes.html')

def contacto(request):
    return render(request, 'ecommerce_coverde/institucional/contacto.html')

def politica_privacidade(request):
    return render(request, 'ecommerce_coverde/institucional/politica_privacidade.html')

def termos_condicoes(request):
    return render(request, 'ecommerce_coverde/institucional/termos_condicoes.html')

def faq(request):
    return render(request, 'ecommerce_coverde/institucional/faq.html')