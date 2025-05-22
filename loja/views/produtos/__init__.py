# loja/views/produtos/__init__.py

from loja.views.lista_produtos import ProdutoListView, CategoriaListagemView
from loja.views.produtos.detalhe import ProdutoDetalheView
from loja.views.produtos.gestao import ProdutoCriarView, ProdutoEditarView

__all__ = [
    'ProdutoListView',
    'CategoriaListagemView',
    'ProdutoDetalheView',
    'ProdutoCriarView',
    'ProdutoEditarView',
]
