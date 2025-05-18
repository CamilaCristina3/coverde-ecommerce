from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Produto

# loja/views/produtos/views.py
class ProdutoListView(ListView):
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

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'pt/produtos/detalhe.html'
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos_relacionados'] = Produto.objects.filter(
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:4]
        return context