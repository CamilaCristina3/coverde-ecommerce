from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from loja.models import Utilizador
from django.contrib.auth.mixins import  UserPassesTestMixin
from loja.models import Produto

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'pt/perfil/perfil.html'

class ConfiguracoesContaView(LoginRequiredMixin, UpdateView):
    model = Utilizador
    fields = [
        'first_name', 'last_name', 'email',
        'telefone', 'morada', 'codigo_postal', 'localidade'
    ]
    template_name = 'pt/perfil/configuracoes.html'
    success_url = reverse_lazy('loja:perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Dados atualizados com sucesso.")
        return super().form_valid(form)


class DashboardProdutorView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'pt/perfil/dashboard_produtor.html'

    def test_func(self):
        return self.request.user.tipo == 'P'  # Apenas produtores

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produtos = Produto.objects.filter(produtor=self.request.user).order_by('-data_criacao')
        context['produtos'] = produtos
        return context