from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse
from decimal import Decimal
from coverde_ecommerce.models import Produto, Pedido, ItemPedido

class CarrinhoView(View):
    template_name = 'coverde_ecommerce/carrinho/carrinho.html'

    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        produtos_no_carrinho = []
        total_geral = Decimal('0.00')
        quantidade_total = 0

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
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
        quantidade = int(request.POST.get('quantidade', 1))

        if quantidade > produto.stock:
            messages.error(request, f"Estoque insuficiente para {produto.nome}")
            return redirect(request.META.get('HTTP_REFERER', reverse('coverde_ecommerce:produto_list')))

        carrinho = request.session.get('carrinho', {})
        produto_key = str(produto.id)
        nova_quantidade = carrinho.get(produto_key, 0) + quantidade

        if nova_quantidade > produto.stock:
            messages.error(request, f"Limite de stock atingido para {produto.nome}.")
            return redirect(request.META.get('HTTP_REFERER', reverse('coverde_ecommerce:produto_list')))

        carrinho[produto_key] = nova_quantidade
        request.session['carrinho'] = carrinho
        request.session.modified = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': sum(carrinho.values()),
                'message': f"{quantidade} × {produto.nome} adicionado ao carrinho!"
            })

        messages.success(request, f"{quantidade} × {produto.nome} adicionado ao carrinho!")
        return redirect(request.META.get('HTTP_REFERER', reverse('coverde_ecommerce:produto_list')))


class CarrinhoAPIView(View):
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
            messages.success(request, f"{produto.nome} removido do carrinho.")

        return redirect('coverde_ecommerce:carrinho')


class AtualizarCarrinhoView(View):
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        carrinho = request.session.get('carrinho', {})
        atualizacoes = request.POST

        for key, valor in atualizacoes.items():
            if key.startswith('quantidade_'):
                produto_id = key.replace('quantidade_', '')
                quantidade = int(valor)

                if quantidade <= 0:
                    carrinho.pop(produto_id, None)
                    continue

                produto = get_object_or_404(Produto, id=produto_id, disponivel=True)

                if quantidade > produto.stock:
                    messages.error(request, f"Máximo disponível de {produto.nome} é {produto.stock}.")
                    continue

                carrinho[produto_id] = quantidade

        request.session['carrinho'] = carrinho
        request.session.modified = True
        messages.success(request, "Carrinho atualizado com sucesso.")
        return redirect('coverde_ecommerce:carrinho')


class LimparCarrinhoView(View):
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        request.session['carrinho'] = {}
        request.session.modified = True
        messages.info(request, "Carrinho esvaziado.")
        return redirect('coverde_ecommerce:carrinho')


# ✅ NOVA VIEW: Checkout
class CheckoutView(View):
    template_name = 'coverde_ecommerce/carrinho/checkout.html'

    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            messages.warning(request, "O seu carrinho está vazio.")
            return redirect('coverde_ecommerce:produto_list')

        itens = []
        total = Decimal('0.00')

        for produto_id, quantidade in carrinho.items():
            produto = get_object_or_404(Produto, id=produto_id)
            subtotal = produto.preco * quantidade
            itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
            total += subtotal

        return render(request, self.template_name, {'itens': itens, 'total': total})

    def post(self, request):
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            messages.warning(request, "O seu carrinho está vazio.")
            return redirect('coverde_ecommerce:produto_list')

        endereco = request.POST.get('endereco')
        metodo = request.POST.get('metodo_pagamento')

        if not endereco or not metodo:
            messages.error(request, "Por favor, preencha todos os campos.")
            return redirect('coverde_ecommerce:checkout')

        total = Decimal('0.00')
        pedido = Pedido.objects.create(
            utilizador=request.user,
            total=0,  # será atualizado após salvar os itens
            endereco_entrega=endereco,
            metodo_pagamento=metodo
        )

        for produto_id, quantidade in carrinho.items():
            produto = get_object_or_404(Produto, id=produto_id)
            subtotal = produto.preco * quantidade
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=produto.preco
            )
            total += subtotal

        pedido.total = total
        pedido.save()

        request.session['carrinho'] = {}
        request.session.modified = True
        messages.success(request, "Pedido realizado com sucesso!")
        return redirect('coverde_ecommerce:pedido_list')  # ou página de sucesso
