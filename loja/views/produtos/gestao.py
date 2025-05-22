from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from loja.models import Produto
from loja.forms import ProdutoForm

class ProdutoCriarView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'pt/produtos/produto_form.html'
    success_url = reverse_lazy('loja:dashboard')

    def form_valid(self, form):
        form.instance.produtor = self.request.user
        messages.success(self.request, "Produto criado com sucesso.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.tipo == 'P'  # Só produtores podem criar


class ProdutoEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'pt/produtos/produto_form.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('loja:dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Produto atualizado com sucesso.")
        return super().form_valid(form)

    def test_func(self):
        produto = self.get_object()
        return self.request.user == produto.produtor
