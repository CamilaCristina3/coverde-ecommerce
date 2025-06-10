from .utilizador import Utilizador
from .produto import Produto
from .categoria import Categoria
from .pedido import Pedido, ItemPedido, Carrinho, ItemCarrinho  # <- importações corretas
from .favorito import Favorito

__all__ = [
    'Utilizador',
    'Produto',
    'Categoria',
    'Pedido',
    'ItemPedido',
    'Carrinho',
    'ItemCarrinho',
    'Favorito',
]
