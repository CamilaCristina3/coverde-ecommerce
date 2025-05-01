from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from loja.models import Produto, Pedido, ItemPedido

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = request.session.get('carrinho', {})

    # Quantidade personalizada
    quantidade = int(request.POST.get('quantidade', 1))

    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        carrinho[produto_id_str] += quantidade
    else:
        carrinho[produto_id_str] = quantidade

    request.session['carrinho'] = carrinho

    # Volta para onde o utilizador estava (continuar a comprar)
    return redirect(request.META.get('HTTP_REFERER', 'produtos'))

    carrinho = request.session.get('carrinho', {})
    carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + 1
    request.session['carrinho'] = carrinho
    messages.success(request, "Produto adicionado ao carrinho!")
    return redirect('ver_carrinho')

@login_required
def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(produto_id), None)
    request.session['carrinho'] = carrinho
    messages.success(request, "Produto removido do carrinho.")
    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    produtos = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=produto_id)
        subtotal = produto.preco * quantidade
        produtos.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'carrinho/ver_carrinho.html', {
        'produtos': produtos,
        'total': total
    })

@login_required
def finalizar_compra(request):
    if request.user.perfil != 'consumidor':
        messages.error(request, "Apenas consumidores podem finalizar compras.")
        return redirect('ver_carrinho')

    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.warning(request, "O carrinho está vazio.")
        return redirect('ver_carrinho')

    pedido = Pedido.objects.create(consumidor=request.user)

    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=produto_id)
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )

    request.session['carrinho'] = {}
    messages.success(request, "Compra finalizada com sucesso!")
    return render(request, 'carrinho/pedido_sucesso.html', {'pedido': pedido})
