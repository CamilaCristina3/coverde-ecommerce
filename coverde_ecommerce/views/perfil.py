from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from coverde_ecommerce.models import Utilizador, Produto, Pedido
from coverde_ecommerce.forms import PerfilUpdateForm, ProdutoForm


class PerfilView(LoginRequiredMixin, DetailView):
    """Visualização detalhada do perfil do usuário com opções de edição"""
    model = Utilizador
    template_name = 'perfil/perfil.html'  # 🔁 Corrigido caminho para refletir estrutura de templates
    context_object_name = 'utilizador'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.tipo == 'C':
            context['total_pedidos'] = Pedido.objects.filter(utilizador=user).count()
        elif user.tipo == 'P':
            context['total_produtos'] = Produto.objects.filter(produtor=user).count()
        return context


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    """Edição de perfil do utilizador autenticado"""
    model = Utilizador
    form_class = PerfilUpdateForm
    template_name = 'perfil/perfil_edit.html'
    success_url = reverse_lazy('coverde_ecommerce:perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Seu perfil foi atualizado com sucesso!'))
        return super().form_valid(form)


class ProdutorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil/dashboard_produtor.html'  # 🔁 Corrigido caminho do template

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != 'P':
            messages.error(request, _('Acesso permitido apenas para produtores'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        produtos = Produto.objects.filter(produtor=user)
        pedidos = Pedido.objects.filter(itens__produto__produtor=user).distinct()

        context.update({
            'produtos_count': produtos.count(),
            'produtos_ativos': produtos.filter(disponivel=True).count(),
            'pedidos_recentes': pedidos.order_by('-data_criacao')[:5],
            'total_vendas': pedidos.filter(status='entregue').aggregate(Sum('total'))['total__sum'] or 0,
            'pedidos_pendentes': pedidos.exclude(status__in=['cancelado', 'entregue']).count(),
            'clientes_unicos': pedidos.values('utilizador').distinct().count(),
        })
        return context


class ConsumidorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil/dashboard_consumidor.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != 'C':
            messages.error(request, _('Acesso permitido apenas para consumidores'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        pedidos = Pedido.objects.filter(utilizador=user)

        context.update({
            'pedidos_ativos': pedidos.exclude(status__in=['cancelado', 'entregue']).count(),
            'historico_pedidos': pedidos.order_by('-data_criacao')[:5],
            'total_gasto': pedidos.filter(status='entregue').aggregate(Sum('total'))['total__sum'] or 0,
            'produtos_favoritos': user.favoritos.count() if hasattr(user, 'favoritos') else 0,
        })
        return context


class AdicionarProdutoView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtor/produto_form.html'  # 🔁 Corrigido caminho

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != 'P':
            messages.error(request, _('Apenas produtores podem adicionar produtos'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.produtor = self.request.user
        messages.success(self.request, _('Produto "%s" adicionado com sucesso!') % form.instance.nome)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('coverde_ecommerce:dashboard_produtor')


class EditarProdutoView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produtor/produto_form.html'
    context_object_name = 'produto'

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != 'P':
            messages.error(request, _('Apenas produtores podem editar produtos'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produto.objects.filter(produtor=self.request.user)

    def get_success_url(self):
        messages.success(self.request, _('Produto "%s" atualizado com sucesso!') % self.object.nome)
        return reverse_lazy('coverde_ecommerce:dashboard_produtor')
