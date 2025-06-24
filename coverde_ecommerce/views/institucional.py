from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """View para a página inicial"""
    template_name = 'coverde_ecommerce/institucional/index.html'

def sobre(request):
    return render(request, 'coverde_ecommerce/institucional/sobre.html')

def solucoes(request):
    return render(request, 'coverde_ecommerce/institucional/solucoes.html')

def contacto(request):
    return render(request, 'coverde_ecommerce/institucional/contacto.html')

def politica_privacidade(request):
    return render(request, 'coverde_ecommerce/institucional/politica_privacidade.html')

def termos_condicoes(request):
    return render(request, 'coverde_ecommerce/institucional/termos_condicoes.html')

def faq(request):
    return render(request, 'coverde_ecommerce/institucional/faq.html')