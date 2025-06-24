from django.views.generic import (TemplateView, DetailView, 
                                UpdateView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from coverde_ecommerce.models import Utilizador, Produto, Pedido, ItemPedido  # ✅ CERTO

from coverde_ecommerce.forms import (PerfilUpdateForm, ProdutoForm)

class PerfilView(LoginRequiredMixin, DetailView):
    """Visualização detalhada do perfil do usuário com opções de edição"""
    model = Utilizador
    template_name = 'coverde_ecommerce/perfil/perfil.html'
    context_object_name = 'utilizador'

    def get_object(self):
        """Retorna sempre o usuário logado"""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Adiciona dados extras ao contexto"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Adiciona estatísticas básicas para o template
        if user.tipo == 'C':
            context['total_pedidos'] = Pedido.objects.filter(utilizador=user).count()
        elif user.tipo == 'P':
            context['total_produtos'] = Produto.objects.filter(produtor=user).count()
        
        return context


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    """View para edição segura do perfil do usuário"""
    model = Utilizador
    form_class = PerfilUpdateForm
    template_name = 'coverde_ecommerce/perfil/perfil_edit.html'
    success_url = reverse_lazy('coverde_ecommerce:perfil')

    def get_object(self):
        """Garante que usuário só edite seu próprio perfil"""
        return self.request.user

    def form_valid(self, form):
        """Adiciona mensagem de sucesso e trata upload de imagem"""
        messages.success(
            self.request, 
            _('Seu perfil foi atualizado com sucesso!')
        )
        return super().form_valid(form)


class ProdutorDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard completo para produtores com métricas de negócio"""
    template_name = 'coverde_ecommerce/produtor/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        """Restringe acesso apenas a produtores"""
        if not request.user.tipo == 'P':
            messages.error(request, _('Acesso permitido apenas para produtores'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Prepara dados estatísticos para o dashboard"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        produtos = Produto.objects.filter(produtor=user)
        pedidos = Pedido.objects.filter(
            itens__produto__produtor=user
        ).distinct().select_related('utilizador')
        
        # Métricas principais
        context.update({
            'produtos_count': produtos.count(),
            'produtos_ativos': produtos.filter(disponivel=True).count(),
            'pedidos_recentes': pedidos.order_by('-data_criacao')[:5],
            'total_vendas': pedidos.filter(status='entregue').aggregate(
                Sum('total')
            )['total__sum'] or 0,
            'pedidos_pendentes': pedidos.exclude(
                status__in=['cancelado', 'entregue']
            ).count(),
            'clientes_unicos': pedidos.values('utilizador').distinct().count(),
        })
        
        return context


class ConsumidorDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard personalizado para consumidores"""
    template_name = 'coverde_ecommerce/consumidor/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        """Garante acesso apenas a consumidores"""
        if not request.user.tipo == 'C':
            messages.error(request, _('Acesso permitido apenas para consumidores'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Prepara dados relevantes para o consumidor"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        pedidos = Pedido.objects.filter(utilizador=user).select_related('endereco_entrega')
        
        context.update({
            'pedidos_ativos': pedidos.exclude(
                status__in=['cancelado', 'entregue']
            ).count(),
            'historico_pedidos': pedidos.order_by('-data_criacao')[:5],
            'total_gasto': pedidos.filter(
                status='entregue'
            ).aggregate(Sum('total'))['total__sum'] or 0,
            'produtos_favoritos': user.favoritos.count(),
        })
        
        return context


class AdicionarProdutoView(LoginRequiredMixin, CreateView):
    """View segura para adição de novos produtos"""
    model = Produto
    form_class = ProdutoForm
    template_name = 'coverde_ecommerceprodutor/produto_form.html'
    success_url = reverse_lazy('coverde_ecommerce:produtor_dashboard')

    def dispatch(self, request, *args, **kwargs):
        """Restringe a produtores"""
        if not request.user.tipo == 'P':
            messages.error(request, _('Apenas produtores podem adicionar produtos'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Associa automaticamente o produtor e valida dados"""
        form.instance.produtor = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, 
            _('Produto "%s" adicionado com sucesso!') % self.object.nome
        )
        return response


class EditarProdutoView(LoginRequiredMixin, UpdateView):
    """View segura para edição de produtos existentes"""
    model = Produto
    form_class = ProdutoForm
    template_name = 'coverde_ecommerce/produtor/produto_form.html'
    context_object_name = 'produto'

    def dispatch(self, request, *args, **kwargs):
        """Restringe a produtores donos do produto"""
        if not request.user.tipo == 'P':
            messages.error(request, _('Apenas produtores podem editar produtos'))
            return redirect('coverde_ecommerce:perfil')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filtra apenas produtos do usuário logado"""
        return super().get_queryset().filter(produtor=self.request.user)

    def get_success_url(self):
        """Feedback e redirecionamento pós-edicao"""
        messages.success(
            self.request, 
            _('Produto "%s" atualizado com sucesso!') % self.object.nome
        )
        return reverse_lazy('coverde_ecommerce:produtor_dashboard')

    def form_valid(self, form):
        """Tratamento adicional para imagens e dados sensíveis"""
        return super().form_valid(form)