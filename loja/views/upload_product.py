from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from loja.models import Produto, Categoria, ImagemProduto
from django.contrib import messages

@login_required
def upload_product_view(request):
    if request.user.perfil != 'produtor':
        messages.error(request, "Apenas produtores podem adicionar produtos.")
        return redirect('homepage')  # ou 'produtos'

    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')
        categoria_id = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        modo_producao = request.POST.get('modo_producao')

        try:
            categoria = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            messages.error(request, "Categoria inválida.")
            return redirect('upload_product')

        produto = Produto.objects.create(
            nome=nome,
            preco=preco,
            quantidade=quantidade,
            categoria=categoria,
            produtor=request.user,
            descricao=descricao,
            modo_producao=modo_producao
        )

        for imagem in request.FILES.getlist('imagens'):
            ImagemProduto.objects.create(produto=produto, imagem=imagem)

        messages.success(request, "Produto adicionado com sucesso!")
        return redirect('produtos')

    categorias = Categoria.objects.all()
    return render(request, 'produtos/upload.html', {'categorias': categorias})
