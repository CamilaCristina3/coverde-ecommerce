# loja/views/produtos/detalhe.py

from django.views.generic import DetailView
from loja.models import Produto

class ProdutoDetalheView(DetailView):
    """Vista para apresentar os detalhes de um produto"""
    model = Produto
    template_name = 'pt/produtos/detalhe.html'
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos_relacionados'] = Produto.objects.filter(
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:4]
        return context
