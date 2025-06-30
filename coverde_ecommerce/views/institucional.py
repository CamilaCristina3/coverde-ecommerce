from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """View para a página inicial"""
    template_name = 'loja/institucional/index.html'

def sobre(request):
    return render(request, 'loja/institucional/sobre.html')

def solucoes(request):
  return render(request, 'loja/Institucional/solucoes.html')


def contacto(request):
    return render(request, 'loja/institucional/contacto.html')

def politica_privacidade(request):
    return render(request, 'loja/institucional/politica_privacidade.html')

def termos_condicoes(request):
    return render(request, 'loja/institucional/termos_condicoes.html')

def faq(request):
    return render(request, 'loja/institucional/faq.html')