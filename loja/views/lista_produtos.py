from django.views.generic import ListView
from loja.models import Produto

class ProdutoListView(ListView):
    """Vista para listar produtos disponíveis com suporte a filtros"""
    model = Produto
    template_name = 'pt/produtos/lista_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Produto.objects.filter(disponivel=True).select_related('categoria')

        # Filtro por categoria via GET (?categoria=frutas)
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__nome__iexact=categoria)

        # Ordenação (?ordenar=preco ou -preco)
        ordenar = self.request.GET.get('ordenar')
        if ordenar in ['preco', '-preco']:
            queryset = queryset.order_by(ordenar)

        # Filtro de disponibilidade explícito (?disponivel=1)
        disponivel = self.request.GET.get('disponivel')
        if disponivel == '1':
            queryset = queryset.filter(disponivel=True)

        return queryset


class CategoriaListagemView(ListView):
    model = Produto
    template_name = 'pt/produtos/lista_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        return Produto.objects.filter(
            disponivel=True,
            categoria__slug=self.kwargs['slug']
        )
