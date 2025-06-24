from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from decimal import Decimal
from ..models import Produto

class CarrinhoView(View):
    """Visualização principal do carrinho com todos os itens e totais"""
    template_name = 'coverde_ecommerce/carrinho/carrinho.html'

    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho', {})
        produtos_no_carrinho = []
        total_geral = Decimal('0.00')
        quantidade_total = 0

        # Obter todos os produtos do carrinho com suas quantidades
        for produto_id, quantidade in carrinho.items():
            produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
            subtotal = produto.preco * Decimal(quantidade)
            
            produtos_no_carrinho.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal
            })
            
            total_geral += subtotal
            quantidade_total += quantidade

        context = {
            'produtos_no_carrinho': produtos_no_carrinho,
            'total_geral': total_geral,
            'quantidade_total': quantidade_total
        }
        
        return render(request, self.template_name, context)


class AdicionarAoCarrinhoView(View):
    """Adiciona itens ao carrinho com verificação de stock"""
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
        quantidade = int(request.POST.get('quantidade', 1))
        
        # Verificar se há estoque suficiente
        if quantidade > produto.stock:
            messages.error(request, f"Quantidade indisponível em stock para {produto.nome}")
            return redirect(request.META.get('HTTP_REFERER', 'coverde_ecommerce:listagem-produto'))
        
        carrinho = request.session.get('carrinho', {})
        produto_key = str(produto.id)
        
        # Verificar se a nova quantidade excede o estoque
        nova_quantidade = carrinho.get(produto_key, 0) + quantidade
        if nova_quantidade > produto.stock:
            messages.error(request, f"Você já tem {carrinho.get(produto_key, 0)} itens no carrinho. Não há estoque suficiente para adicionar mais {quantidade}.")
            return redirect(request.META.get('HTTP_REFERER', 'coverde_ecommerce:listagem-produto'))
        
        # Atualizar carrinho
        carrinho[produto_key] = nova_quantidade
        request.session['carrinho'] = carrinho
        request.session.modified = True
        
        # Resposta para AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': sum(carrinho.values()),
                'message': f"{quantidade} × {produto.nome} adicionado ao carrinho!"
            })
        
        messages.success(request, f"{quantidade} × {produto.nome} adicionado ao carrinho!")
        return redirect(request.META.get('HTTP_REFERER', 'coverde_ecommerce:listagem-produto'))

    class CarrinhoAPIView(View):
     """API para operações com o carrinho"""
    
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        produtos = []
        total = Decimal('0.00')
        
        for produto_id, quantidade in carrinho.items():
            produto = get_object_or_404(Produto, id=produto_id)
            subtotal = produto.preco * Decimal(quantidade)
            produtos.append({
                'id': produto.id,
                'nome': produto.nome,
                'preco': str(produto.preco),
                'quantidade': quantidade,
                'subtotal': str(subtotal),
                'imagem': produto.imagem.url if produto.imagem else None
            })
            total += subtotal
        
        return JsonResponse({
            'success': True,
            'produtos': produtos,
            'total': str(total),
            'total_itens': sum(carrinho.values())
        })


class RemoverDoCarrinhoView(View):
    """Remove itens do carrinho completamente"""
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})
        
        if str(produto_id) in carrinho:
            del carrinho[str(produto_id)]
            request.session['carrinho'] = carrinho
            request.session.modified = True
            messages.success(request, f"{produto.nome} removido do carrinho")
        
        return redirect('carrinho')


class AtualizarCarrinhoView(View):
    """Atualiza quantidades no carrinho com verificação de stock"""
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        carrinho = request.session.get('carrinho', {})
        atualizacoes = request.POST
        
        for produto_id, quantidade in atualizacoes.items():
            if produto_id.startswith('quantidade_'):
                produto_id = produto_id.replace('quantidade_', '')
                quantidade = int(quantidade)
                
                if quantidade <= 0:
                    if produto_id in carrinho:
                        del carrinho[produto_id]
                    continue
                
                produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
                
                if quantidade > produto.stock:
                    messages.error(request, f"stock insuficiente para {produto.nome} (máx: {produto.stock})")
                    continue
                
                carrinho[produto_id] = quantidade
        
        request.session['carrinho'] = carrinho
        request.session.modified = True
        messages.success(request, "Carrinho atualizado com sucesso")
        return redirect('carrinho')


class LimparCarrinhoView(View):
    """Esvazia o carrinho completamente"""
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        request.session['carrinho'] = {}
        request.session.modified = True
        messages.info(request, "Seu carrinho foi esvaziado")
        return redirect('carrinho')