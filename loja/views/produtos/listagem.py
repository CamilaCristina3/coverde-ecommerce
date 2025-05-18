# loja/views/produtos/listagem.py

from django.views.generic import ListView
from loja.models import Produto

class ProdutoListView(ListView):
    """Vista para listar todos os produtos disponíveis"""
    model = Produto
    template_name = 'pt/produtos/listagem.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(disponivel=True)
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__nome=categoria)
        return queryset

class CategoriaListagemView(ListView):
    """Vista para listar produtos de uma categoria específica"""
    model = Produto
    template_name = 'pt/produtos/listagem_categoria.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        return Produto.objects.filter(
            disponivel=True,
            categoria__slug=self.kwargs['slug']
        )
