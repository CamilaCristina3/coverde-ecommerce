from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from ..models import Categoria

class CategoriaAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin comum para views administrativas"""
    def test_func(self):
        return self.request.user.is_superuser

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'ecommerce_coverde/categoria/listagem.html'
    context_object_name = 'categorias'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        return queryset

class CategoriaCreateView(CategoriaAdminMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    template_name = 'ecommerce_coverde/categoria/formulario.html'
    fields = ['nome', 'descricao', 'icone', 'ordem_menu']
    success_url = reverse_lazy('ecommerce_coverde:categoria_listagem')
    success_message = _('Categoria criada com sucesso!')

class CategoriaUpdateView(CategoriaAdminMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    template_name = 'ecommerce_coverde/categoria/formulario.html'
    fields = ['nome', 'descricao', 'icone', 'ordem_menu']
    success_url = reverse_lazy('ecommerce_coverde:categoria_listagem')
    success_message = _('Categoria atualizada com sucesso!')

class CategoriaDeleteView(CategoriaAdminMixin, SuccessMessageMixin, DeleteView):
    model = Categoria
    template_name = 'ecommerce_coverde/categoria/confirmar_exclusao.html'
    success_url = reverse_lazy('ecommerce_coverde:categoria_listagem')
    success_message = _('Categoria excluída com sucesso!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos_relacionados'] = self.object.produtos.count()
        return context
    # Exemplo em views.py
def base_context(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}

categorias = Categoria.objects.prefetch_related('produto_set').all()

from django.core.cache import cache

def get_categorias():
    categorias = cache.get('todas_categorias')
    if not categorias:
        categorias = list(Categoria.objects.all())
        cache.set('todas_categorias', categorias, 3600)  # Cache por 1 hora
    return categorias