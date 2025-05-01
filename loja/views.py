from django.shortcuts import render
from django.views import View
from loja.models import Produto, Categoria, produtos  # nomes corretos dos modelos

# Página inicial com produtos e categorias
class Index(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        produtos = Produto.objects.all()
        user = request.user
        return render(request, "index.html", {
            "categorias": categorias,
            "produtos": produtos,
            "user": user
        })

# Página da loja com filtro de categoria
def loja(request):
    categoria_id = request.GET.get('categoria')
    categorias = Categoria.objects.all()

    if categoria_id:
        produtos = Produto.objects.filter(categoria_id=categoria_id)
    else:
        produtos = Produto.objects.all()

    return render(request, 'index.html', {
        'produtos': produtos,
        'categorias': categorias
    })
# views.py
def lista_produtos(request):
    # lógica para exibir os produtos
    return render(request, 'produtos.html', {'produtos': produtos})
