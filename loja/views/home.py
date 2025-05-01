from django.shortcuts import render, redirect
from loja.models import User, Produto, Categoria

from django.views import View

# Página principal com todos os produtos e categorias
class Index(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        produtos = Produto.objects.all()
        user = request.user
        return render(request, "index.html", {"categorias": categorias, "produtos": produtos, "user": user})

# Página loja com filtro por categoria (ex: ?categoria=2)
def loja(request):
    categoria_id = request.GET.get('categoria')
    categorias = Categoria.objects.all()

    if categoria_id:
        produtos = Produto.objects.filter(categoria_id=categoria_id)
    else:
        produtos = Produto.objects.all()

    context = {
        'produtos': produtos,
        'categorias': categorias
    }

    return render(request, 'index.html', context)
