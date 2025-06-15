from django.urls import path
from django.contrib.auth import views as auth_views


from ecommerce_coverde.views import IndexView
from ecommerce_coverde.views.auth import (
    # Views de Autenticação
    LoginView,  
    custom_logout, 
    registration_choice,
    signup_produtor, 
    signup_consumidor
)

from ecommerce_coverde.views.carrinho import (
    CarrinhoView, AdicionarAoCarrinhoView, RemoverDoCarrinhoView,
    AtualizarCarrinhoView, LimparCarrinhoView  # Adicione aqui
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

from ecommerce_coverde.views.perfil import (
    AdicionarProdutoView,
    ConsumidorDashboardView,
    EditarProdutoView,
    PerfilView,
    PerfilUpdateView,
    ProdutorDashboardView
)
from ecommerce_coverde.views import (
   
    # Favoritos
    FavoritosListView, adicionar_favorito, remover_favorito,
   
)
from ecommerce_coverde.views.produto import (
    ProdutoListView, ProdutoDetailView, ProdutoSearchView,
    AdicionarFavoritoView, ProdutoJSONView
)


from ecommerce_coverde.views.pedido import (
    PedidoListView, PedidoDetailView, PedidoCreateView,
    PedidoUpdateView, PedidoCancelView,
    CheckoutView, CheckoutSuccessView  # ✅ Adicione isto
)

app_name = 'ecommerce_coverde'

urlpatterns = [
    # ===== PÁGINAS INSTITUCIONAIS =====
     path('', IndexView.as_view(), name='index'),
    path('sobre/', sobre, name='sobre'),
    path('solucoes/', solucoes, name='solucoes'),
    path('contacto/', contacto, name='contacto'),
    path('politica-privacidade/', politica_privacidade, name='politica_privacidade'),
    path('termos-condicoes/', termos_condicoes, name='termos_condicoes'),
    path('faq/', faq, name='faq'),

    # ===== AUTENTICAÇÃO E REGISTO =====
  path("conta/entrar/", LoginView.as_view(), name="login"),
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

    # ===== ALTERAÇÃO DE SENHA (NOVAS URLs) =====
    path('conta/alterar-passe/', auth_views.PasswordChangeView.as_view(
        template_name='ecommerce_coverde/registration/password_change_pt.html'
    ), name='password_change'),
    
    path('conta/alterar-passe/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='ecommerce_coverde/registration/password_change_done_pt.html'
    ), name='password_change_done'),

    # ===== PERFIL E DASHBOARDS =====
path('perfil/', PerfilView.as_view(), name='perfil'),
path('perfil/editar/', PerfilUpdateView.as_view(), name='perfil-edit'),
path('dashboard/produtor/', ProdutorDashboardView.as_view(), name='produtor_dashboard'),
path('dashboard/consumidor/', ConsumidorDashboardView.as_view(), name='consumidor_dashboard'),
path('produto/adicionar/', AdicionarProdutoView.as_view(), name='adicionar_produto'),
path('produto/editar/<int:produto_id>/', EditarProdutoView.as_view(), name='editar_produto'),

    # ===== CATEGORIAS =====
path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
 path('categorias/criar/', CategoriaCreateView.as_view(), name='categoria-create'),
path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria-update'),
path('categorias/<int:pk>/excluir/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    path('categoria/<slug:slug>/', ProdutoListView.as_view(), name='produto-por-categoria'),

    # ===== PRODUTOS =====
    path('produtos/', ProdutoListView.as_view(), name='listagem-produto'),
    path('produtos/<slug:slug>/', ProdutoDetailView.as_view(), name='detalhe-produto'),
    path('produtos/busca/', ProdutoSearchView.as_view(), name='produto-busca'),
    path('produtos/<int:produto_id>/favorito/', AdicionarFavoritoView.as_view(), name='produto-favorito'),
    path('api/produtos/', ProdutoJSONView.as_view(), name='produto-json'),

    # ===== PEDIDOS =====
    path('pedidos/', PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/criar/', PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedidos/<int:pk>/atualizar/', PedidoUpdateView.as_view(), name='pedido-update'),
    path('pedidos/<int:pk>/cancelar/', PedidoCancelView.as_view(), name='pedido-cancel'),

       # ===== CARRINHO =====
       path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', AdicionarAoCarrinhoView.as_view(), name='add_to_cart'),
    path('carrinho/remover/<int:produto_id>/', RemoverDoCarrinhoView.as_view(), name='remove-from-cart'),
    path('carrinho/atualizar/', AtualizarCarrinhoView.as_view(), name='update-cart'),
   
    
    # ===== CHECKOUT =====
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/sucesso/<str:codigo>/', CheckoutSuccessView.as_view(), name='checkout-success'),

    # ===== FAVORITOS =====
    path('favoritos/', FavoritosListView.as_view(), name='favorito_list'),
    path('favoritos/adicionar/<int:produto_id>/', adicionar_favorito, name='adicionar_favorito'),
    path('favoritos/remover/<int:produto_id>/', remover_favorito, name='remover_favorito'),
]
