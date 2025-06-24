from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from coverde_ecommerce.models import Produto, Favorito  # Importação absoluta recomendada

class ProdutoListView(ListView):
    model = Produto
    template_name = 'coverde_ecommerce/produto/listagem-produto.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        return Produto.objects.filter(disponivel=True)

class ProdutoDetailView(DetailView):
     model = Produto
     template_name = 'coverde_ecommerce/produto/detalhe-produto.html'
     slug_url_kwarg = 'slug'  # Isso define que o parâmetro na URL é 'slug'
     slug_field = 'slug'
     context_object_name = 'produto'

class ProdutoSearchView(ListView):
    template_name = 'produto/busca.html'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Produto.objects.filter(
            nome__icontains=query,
            disponivel=True
        )

class AdicionarFavoritoView(LoginRequiredMixin, View):
    def post(self, request, produto_id):
        produto = Produto.objects.get(id=produto_id)
        favorito, created = Favorito.objects.get_or_create(
            utilizador=request.user,
            produto=produto
        )
        if not created:
            favorito.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})

class ProdutoJSONView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        produtos = Produto.objects.filter(
            nome__icontains=query,
            disponivel=True
        ).values('id', 'nome', 'preco')[:10]
        return JsonResponse({'produtos': list(produtos)})