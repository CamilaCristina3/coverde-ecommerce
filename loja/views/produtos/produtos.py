# loja/views/produtos/produtos.py

from django.shortcuts import render, get_object_or_404  # ← IMPORTAÇÃO CORRIGIDA
from loja.models import Produto, Categoria

def produto_detail(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produtos/detalhe_produto.html', {'produto': produto})

def lista_produtos(request):
    categoria_id = request.GET.get('categoria')

    if categoria_id:
        produtos = Produto.objects.filter(categoria_id=categoria_id, produtor__is_active=True)
    else:
        produtos = Produto.objects.filter(produtor__is_active=True)

    categorias = Categoria.objects.all()

    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'categorias': categorias
    })
