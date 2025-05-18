from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

# --- Autenticação ---
from loja.views.auth.login import LoginView
from loja.views.auth.registo import SignupConsumidorView, SignupProdutorView
from loja.views.auth.verificacao_email import SignupEmailVerificationView
from loja.views.auth.logout import logout_view

# --- Páginas principais ---
from loja.views.home import IndexView, LojaView

# --- Produtos (views organizadas por funcionalidade) ---
from loja.views.produtos.listagem import ProdutoListView, CategoriaListagemView
from loja.views.produtos.detalhe import ProdutoDetalheView
from loja.views.produtos.gestao import ProdutoCriarView, ProdutoEditarView

# --- Carrinho ---
from loja.views.carrinho import (
    CarrinhoView,
    AdicionarAoCarrinhoView,
    RemoverDoCarrinhoView,
    FinalizarCompraView
)


# --- Perfil ---
from loja.views.perfil import (
    PerfilView,
    DashboardProdutorView,
    ConfiguracoesContaView
)

# --- Institucional ---
from loja.views.institucional import (
    SobreView,
    ContactosView,
    PoliticaPrivacidadeView,
    ComoFuncionaView
)

urlpatterns = [
    # --- Páginas principais ---
    path('', IndexView.as_view(), name='index'),
    path('loja/', LojaView.as_view(), name='loja'),

    # --- Autenticação ---
    path('conta/', include([
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', logout_view, name='logout'),
        path('registar/', include([
            path('consumidor/', SignupConsumidorView.as_view(), name='registar_consumidor'),
            path('produtor/', SignupProdutorView.as_view(), name='registar_produtor'),
        ])),
        path('verificar-email/', SignupEmailVerificationView.as_view(), name='verificar_email'),

        # Recuperação de palavra-passe
        path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='pt/auth/password_reset.html',
            email_template_name='pt/auth/password_reset_email.html',
            subject_template_name='pt/auth/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done')
        ), name='password_reset'),
        path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='pt/auth/password_reset_done.html'
        ), name='password_reset_done'),
        path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='pt/auth/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ), name='password_reset_confirm'),
        path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='pt/auth/password_reset_complete.html'
        ), name='password_reset_complete'),
    ])),

    # --- Produtos ---
    path('produtos/', include([
        path('gerir/', include([
            path('adicionar/', ProdutoCriarView.as_view(), name='adicionar_produto'),
            path('editar/<slug:slug>/', ProdutoEditarView.as_view(), name='editar_produto'),
        ])),
        path('categoria/<slug:slug>/', CategoriaListagemView.as_view(), name='categoria'),
        path('', ProdutoListView.as_view(), name='produtos'),
        path('<slug:slug>/', ProdutoDetalheView.as_view(), name='detalhe_produto'),
    ])),

    # --- Carrinho ---
    path('carrinho/', include([
        path('', CarrinhoView.as_view(), name='carrinho'),
        path('item/', include([
            path('adicionar/<slug:produto_slug>/', AdicionarAoCarrinhoView.as_view(), name='adicionar_carrinho'),
            path('remover/<slug:produto_slug>/', RemoverDoCarrinhoView.as_view(), name='remover_carrinho'),
        ])),
        path('checkout/', FinalizarCompraView.as_view(), name='checkout'),
    ])),

    # --- Perfil e Dashboard ---
    path('conta/perfil/', include([
        path('', PerfilView.as_view(), name='perfil'),
        path('configuracoes/', ConfiguracoesContaView.as_view(), name='configuracoes_conta'),
    ])),
    path('dashboard/', DashboardProdutorView.as_view(), name='dashboard'),

    # --- Institucional ---
    path('sobre-nos/', include([
        path('', SobreView.as_view(), name='sobre'),
        path('como-funciona/', ComoFuncionaView.as_view(), name='como_funciona'),
    ])),
    path('contactos/', ContactosView.as_view(), name='contactos'),
    path('politica-privacidade/', PoliticaPrivacidadeView.as_view(), name='politica_privacidade'),

    # --- Legal ---
    path('legal/', include([
        path('termos-servico/', TemplateView.as_view(
            template_name='pt/institucional/termos_servico.html'
        ), name='termos_servico'),
        path('politica-cookies/', TemplateView.as_view(
            template_name='pt/institucional/politica_cookies.html'
        ), name='politica_cookies'),
    ])),
]
