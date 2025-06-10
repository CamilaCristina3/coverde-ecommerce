# ecommerce_coverde/views/carrinho.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from ..models import Produto, Carrinho

class CarrinhoView(LoginRequiredMixin, View):
    """View para exibir o carrinho do usuário"""
    def get(self, request):
        itens_carrinho = Carrinho.objects.filter(utilizador=request.user).select_related('produto')
        total = sum(item.subtotal() for item in itens_carrinho)
        
        return render(request, 'ecommerce_coverde/carrinho/carrinho.html', {
            'itens_carrinho': itens_carrinho,
            'total': total
        })

class AdicionarAoCarrinhoView(LoginRequiredMixin, View):
    """View para adicionar itens ao carrinho"""
    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        
        # Verifica se há estoque disponível
        if produto.quantidade < 1:
            messages.warning(request, 'Este produto está indisponível no momento.')
            return redirect('ecommerce_coverde:produto-detalhe', slug=produto.slug)
        
        carrinho_item, created = Carrinho.objects.get_or_create(
            utilizador=request.user,
            produto=produto,
            defaults={'quantidade': 1}
        )
        
        if not created:
            if carrinho_item.quantidade < produto.quantidade:
                carrinho_item.quantidade += 1
                carrinho_item.save()
                messages.success(request, f'Mais uma unidade de {produto.nome} foi adicionada ao seu carrinho!')
            else:
                messages.warning(request, f'Quantidade máxima disponível de {produto.nome} já está no seu carrinho.')
        else:
            messages.success(request, f'{produto.nome} foi adicionado ao seu carrinho!')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'carrinho_count': Carrinho.objects.carrinho_count(request.user)
            })
            
        return redirect('ecommerce_coverde:carrinho')

class RemoverDoCarrinhoView(LoginRequiredMixin, View):
    """View para remover itens do carrinho"""
    def post(self, request, item_id):
        carrinho_item = get_object_or_404(Carrinho, id=item_id, utilizador=request.user)
        produto_nome = carrinho_item.produto.nome
        carrinho_item.delete()
        
        messages.success(request, f'{produto_nome} foi removido do seu carrinho!')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'carrinho_count': Carrinho.objects.carrinho_count(request.user)
            })
            
        return redirect('ecommerce_coverde:carrinho')

class AtualizarCarrinhoView(LoginRequiredMixin, View):
    """View para atualizar quantidades no carrinho"""
    def post(self, request, item_id):
        carrinho_item = get_object_or_404(Carrinho, id=item_id, utilizador=request.user)
        nova_quantidade = int(request.POST.get('quantidade', 1))
        
        if nova_quantidade < 1:
            carrinho_item.delete()
            messages.success(request, f'{carrinho_item.produto.nome} foi removido do seu carrinho!')
        else:
            if nova_quantidade > carrinho_item.produto.quantidade:
                messages.warning(request, f'Quantidade indisponível para {carrinho_item.produto.nome}. Máximo: {carrinho_item.produto.quantidade}')
                nova_quantidade = carrinho_item.produto.quantidade
            
            carrinho_item.quantidade = nova_quantidade
            carrinho_item.save()
            messages.success(request, f'Quantidade de {carrinho_item.produto.nome} atualizada!')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'carrinho_count': Carrinho.objects.carrinho_count(request.user),
                'subtotal': carrinho_item.subtotal() if nova_quantidade > 0 else 0,
                'total': sum(item.subtotal() for item in Carrinho.objects.filter(utilizador=request.user))
            })
            
        return redirect('ecommerce_coverde:carrinho')

class LimparCarrinhoView(LoginRequiredMixin, View):
    """View para limpar completamente o carrinho"""
    def post(self, request):
        Carrinho.objects.filter(utilizador=request.user).delete()
        messages.success(request, 'Seu carrinho foi esvaziado com sucesso!')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'carrinho_count': 0
            })
            
        return redirect('ecommerce_coverde:carrinho')