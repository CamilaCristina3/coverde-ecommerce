# Exportações principais
from .index import IndexView

# Exportações de autenticação
from .auth import (
    LoginView, custom_logout, registration_choice,
    signup_produtor, signup_consumidor
)

# Exportações de perfil
from .perfil import (
    PerfilView, PerfilUpdateView, ProdutorDashboardView,
    ConsumidorDashboardView, AdicionarProdutoView, EditarProdutoView
)

# Exportações de favoritos
from .favoritos import (
    FavoritosListView, adicionar_favorito, remover_favorito
)

# Exportações institucionais
from .institucional import (
    faq, sobre, solucoes, contacto,
    politica_privacidade, termos_condicoes
)

__all__ = [
    'IndexView',
    'LoginView', 'custom_logout', 'registration_choice',
    'signup_produtor', 'signup_consumidor',
    'PerfilView', 'PerfilUpdateView', 'ProdutorDashboardView',
    'ConsumidorDashboardView', 'AdicionarProdutoView', 'EditarProdutoView',
    'FavoritosListView', 'adicionar_favorito', 'remover_favorito',
    'faq', 'sobre', 'solucoes', 'contacto',
    'politica_privacidade', 'termos_condicoes'
]