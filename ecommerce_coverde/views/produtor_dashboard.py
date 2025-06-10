from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..models import Produto

class EditarProdutoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Apenas produtor dono do produto pode editar"""
    model = Produto
    template_name = 'dashboard/editar_produto.html'
    fields = ['nome', 'preco', 'estoque']

    def test_func(self):
        produto = self.get_object()
        return self.request.user == produto.produtor