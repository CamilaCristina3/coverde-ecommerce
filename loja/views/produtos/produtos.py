from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from loja.models import Produto

class ListaProdutosView(ListView):
    model = Produto
    template_name = 'pt/shared/produtos/listagem.html'  # Mantido original
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(disponivel=True)
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__nome=categoria)
        return queryset

class DetalheProdutoView(DetailView):
    model = Produto
    template_name = 'pt/shared/produto/detalhe.html'  # Corrigido aqui
    context_object_name = 'produto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione produtos relacionados ao contexto
        context['produtos_similares'] = Produto.objects.filter(
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:4]
        return context