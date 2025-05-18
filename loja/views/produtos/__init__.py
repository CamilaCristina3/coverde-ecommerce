# loja/views/produtos/__init__.py

from .listagem import ProdutoListView, CategoriaListagemView
from .detalhe import ProdutoDetalheView
from .gestao import ProdutoCriarView, ProdutoEditarView

__all__ = [
    'ProdutoListView',
    'CategoriaListagemView',
    'ProdutoDetalheView',
    'ProdutoCriarView',
    'ProdutoEditarView',
]
