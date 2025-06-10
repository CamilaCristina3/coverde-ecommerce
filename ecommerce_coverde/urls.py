from django.urls import path
from django.contrib.auth import views as auth_views

from . import views  # apenas necessário se ainda usa views institucionais antigas
from .views import pedido_views
from .views.carrinho import (
    CarrinhoView, AdicionarAoCarrinhoView, RemoverDoCarrinhoView,
    AtualizarCarrinhoView, LimparCarrinhoView
)
from .views.categoria import (
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
)
from .views.institucional import (
    faq,
    sobre,
    solucoes,
    contacto,
    politica_privacidade,
    termos_condicoes,
)


from ecommerce_coverde.views.index import Index
from ecommerce_coverde.views.auth import (
    login_view, custom_logout, registration_choice,
    signup_produtor, signup_consumidor
)
from ecommerce_coverde.views.perfil import (
    PerfilView, ProdutorDashboardView, ConsumidorDashboardView,
    AdicionarProdutoView, EditarProdutoView
)
from ecommerce_coverde.views import (
    FavoritosListView, adicionar_favorito, remover_favorito
)
from ecommerce_coverde.views.produto import (
    ProdutoListView, ProdutoDetailView, ProdutoSearchView,
    AdicionarFavoritoView, ProdutoJSONView
)

app_name = 'ecommerce_coverde'

urlpatterns = [
    # ===== PÁGINAS INSTITUCIONAIS =====
    path('', Index.as_view(), name='index'),
    path('sobre/', sobre, name='sobre'),
    path('solucoes/', solucoes, name='solucoes'),
    path('contacto/', contacto, name='contacto'),
    path('politica-privacidade/', politica_privacidade, name='politica_privacidade'),
    path('termos-condicoes/', termos_condicoes, name='termos_condicoes'),
    path('faq/', faq, name='faq'),

    # ===== AUTENTICAÇÃO E REGISTO =====
    path("conta/entrar/", login_view, name="login"),
    path("conta/sair/", custom_logout, name="logout"),
    path("conta/registar/", registration_choice, name="registration_choice"),
    path("conta/registar/produtor/", signup_produtor, name="signup_produtor"),
    path("conta/registar/consumidor/", signup_consumidor, name="signup_consumidor"),

    # ===== RECUPERAÇÃO DE SENHA =====
    path('conta/recuperar-passe/', auth_views.PasswordResetView.as_view(
        template_name='ecommerce_coverde/registration/password_reset_pt.html',
        email_template_name='ecommerce_coverde/registration/password_reset_email_pt.html',
        subject_template_name='ecommerce_coverde/registration/password_reset_subject_pt.txt'
    ), name='password_reset'),

    path('conta/recuperar-passe/concluido/', auth_views.PasswordResetDoneView.as_view(
        template_name='ecommerce_coverde/registration/password_reset_done_pt.html'
    ), name='password_reset_done'),

    path('conta/recuperar-passe/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='ecommerce_coverde/registration/password_reset_confirm_pt.html'
    ), name='password_reset_confirm'),

    path('conta/recuperar-passe/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='ecommerce_coverde/registration/password_reset_complete_pt.html'
    ), name='password_reset_complete'),

    # ===== PERFIL E DASHBOARDS =====
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('dashboard/produtor/', ProdutorDashboardView.as_view(), name='produtor_dashboard'),
    path('dashboard/consumidor/', ConsumidorDashboardView.as_view(), name='consumidor_dashboard'),
    path('produto/adicionar/', AdicionarProdutoView.as_view(), name='adicionar_produto'),
    path('produto/editar/<int:produto_id>/', EditarProdutoView.as_view(), name='editar_produto'),

    # ===== CATEGORIAS =====
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/criar/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/excluir/', CategoriaDeleteView.as_view(), name='categoria-delete'),

    # ===== PRODUTOS =====
    path('produtos/', ProdutoListView.as_view(), name='listagem-produto'),
    path('produtos/<slug:slug>/', ProdutoDetailView.as_view(), name='detalhe-produto'),
    path('produtos/busca/', ProdutoSearchView.as_view(), name='produto-busca'),
    path('produtos/<int:produto_id>/favorito/', AdicionarFavoritoView.as_view(), name='produto-favorito'),
    path('api/produtos/', ProdutoJSONView.as_view(), name='produto-json'),

    # ===== PEDIDOS =====
    path('pedidos/', pedido_views.PedidoListView.as_view(), name='pedido-list'),
    path('pedidos/criar/', pedido_views.PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidos/<int:pk>/', pedido_views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedidos/<int:pk>/atualizar/', pedido_views.PedidoUpdateView.as_view(), name='pedido-update'),
    path('pedidos/<int:pk>/cancelar/', pedido_views.PedidoCancelView.as_view(), name='pedido-cancel'),

    # ===== CARRINHO =====
    path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', AdicionarAoCarrinhoView.as_view(), name='add-to-cart'),
    path('carrinho/remover/<int:produto_id>/', RemoverDoCarrinhoView.as_view(), name='remove-from-cart'),
    path('carrinho/limpar/', LimparCarrinhoView.as_view(), name='clear-cart'),

    # ===== CHECKOUT =====
    path('checkout/', pedido_views.CheckoutView.as_view(), name='checkout'),
    path('checkout/sucesso/<str:codigo>/', pedido_views.CheckoutSuccessView.as_view(), name='checkout-success'),

    # ===== FAVORITOS =====
    path('favoritos/', FavoritosListView.as_view(), name='favoritos'),
    path('favoritos/adicionar/<int:produto_id>/', adicionar_favorito, name='adicionar_favorito'),
    path('favoritos/remover/<int:produto_id>/', remover_favorito, name='remover_favorito'),
]
