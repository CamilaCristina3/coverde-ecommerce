# loja/views/produtos/gestao.py

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from loja.models import Produto

class ProdutoCriarView(CreateView):
    """Vista para criação de um novo produto"""
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'categoria', 'imagem']
    template_name = 'pt/produtos/formulario.html'
    success_url = reverse_lazy('produtos')

class ProdutoEditarView(UpdateView):
    """Vista para edição de um produto existente"""
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'categoria', 'imagem']
    template_name = 'pt/produtos/formulario.html'
    success_url = reverse_lazy('produtos')
