from django.urls import path

# Autenticação
from loja.views.auth.login import Login
from loja.views.auth.signup_email import SignupEmailCheck
from loja.views.auth.signup_continue import SignupContinue
from loja.views.auth.logout import logout_view

# Páginas principais
from loja.views.home import Index, loja

# Produtos e categorias
from loja.views.produtos.categoria import CategoriaView
from loja.views.produtos.produtos import lista_produtos, produto_detail
from loja.views.upload_product import upload_product_view

# Carrinho de compras
from loja.views.carrinho import (
    adicionar_ao_carrinho,
    remover_do_carrinho,
    ver_carrinho,
    finalizar_compra,
)

# Utilizador
from loja.views.user import UserView

# Contacto
from loja.views.contactos import contactos_view

# Institucional
from loja.views.paginas import (
    quem_somos,
    como_funciona,
    novidades,
    fala_connosco,
    politica_privacidade,
)

urlpatterns = [
    # Página inicial
    path('', Index.as_view(), name='homepage'),

    # Loja
    path('loja/', loja, name='loja'),

    # Autenticação
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/email/', SignupEmailCheck.as_view(), name='signup_email'),
    path('signup/continue/', SignupContinue.as_view(), name='signup_continue'),

    # Produtos
    path('produtos/', lista_produtos, name='produtos'),
    path('produto/<int:id>/', produto_detail, name='produto_detail'),
    path('upload-product/', upload_product_view, name='upload_product'),

    # Carrinho
      path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('carrinho/finalizar/', finalizar_compra, name='finalizar_compra'),
    # Utilizador
    path('user/', UserView.as_view(), name='user'),

    # Institucional e contacto
    path('quem-somos/', quem_somos, name='quem_somos'),
    path('como-funciona/', como_funciona, name='como_funciona'),
    path('novidades/', novidades, name='novidades'),
    path('fala-connosco/', fala_connosco, name='fala_connosco'),
    path('contactos/', contactos_view, name='contactos'),
    path('politica-privacidade/', politica_privacidade, name='politica_privacidade'),
]
