# loja/views/produtos/listagem.py

from django.views.generic import ListView
from loja.models import Produto

class ProdutoListView(ListView):
    """
    Lista geral de produtos disponíveis com suporte a:
    - Filtro por categoria (?categoria=...)
    - Filtro por disponibilidade (?disponivel=1)
    - Ordenação (?ordenar=preco ou -preco)
    """
    model = Produto
    template_name = 'pt/produtos/lista_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Produto.objects.filter(disponivel=True).select_related('categoria')

        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__nome__iexact=categoria)

        ordenar = self.request.GET.get('ordenar')
        if ordenar in ['preco', '-preco']:
            queryset = queryset.order_by(ordenar)

        if self.request.GET.get('disponivel') == '1':
            queryset = queryset.filter(disponivel=True)

        return queryset


class CategoriaListagemView(ListView):
    """
    Lista produtos filtrados por slug da categoria na URL
    """
    model = Produto
    template_name = 'pt/produtos/lista_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        return Produto.objects.filter(
            disponivel=True,
            categoria__slug=self.kwargs['slug']
        )
