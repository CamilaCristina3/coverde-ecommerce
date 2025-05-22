from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# --- Autenticação ---
from loja.views.auth.login import LoginView
from loja.views.auth.registo import SignupConsumidorView, SignupProdutorView
from loja.views.auth.verificacao_email import SignupEmailVerificationView
from loja.views.auth.logout import logout_view

# --- Páginas principais ---
from loja.views.home import IndexView, LojaView

# --- Produtos ---
from loja.views.lista_produtos import ProdutoListView, CategoriaListagemView
from loja.views.produtos.detalhe import ProdutoDetalheView
from loja.views.produtos.gestao import ProdutoCriarView, ProdutoEditarView

# --- Carrinho ---
from loja.views.carrinho import (
    CarrinhoView,
    AdicionarAoCarrinhoView,
    RemoverDoCarrinhoView,
    FinalizarCompraView,
)

# --- Perfil ---
from loja.views.perfil import (
    PerfilView,
    ConfiguracoesContaView,
    DashboardProdutorView,
)

# --- Institucional ---
from loja.views.institucional import (
    SobreView,
    ContactosView,
    PoliticaPrivacidadeView,
    ComoFuncionaView,
)

app_name = "loja"

urlpatterns = [
    # Página Inicial
    path('', IndexView.as_view(), name='index'),
    path('loja/', LojaView.as_view(), name='loja'),

    # Autenticação
    path('conta/login/', LoginView.as_view(), name='login'),
    path('conta/logout/', logout_view, name='logout'),
    path('conta/signup/consumidor/', SignupConsumidorView.as_view(), name='signup_consumidor'),
    path('conta/signup/produtor/', SignupProdutorView.as_view(), name='signup_produtor'),
    path('conta/verificar-email/', SignupEmailVerificationView.as_view(), name='verificar_email'),

    # Recuperação de Senha
    path('conta/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='pt/auth/password_reset.html',
        email_template_name='pt/auth/password_reset_email.html',
        subject_template_name='pt/auth/password_reset_subject.txt',
        success_url=reverse_lazy('loja:password_reset_done')
    ), name='password_reset'),
    path('conta/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pt/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('conta/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pt/auth/password_reset_confirm.html',
        success_url=reverse_lazy('loja:password_reset_complete')
    ), name='password_reset_confirm'),
    path('conta/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pt/auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Produtos
    path('produtos/', ProdutoListView.as_view(), name='produtos'),
    path('produtos/categoria/<slug:slug>/', CategoriaListagemView.as_view(), name='categoria'),
    path('produtos/<slug:slug>/', ProdutoDetalheView.as_view(), name='detalhe_produto'),

    # Gestão de Produtos (apenas para produtores)
    path('produtos/gerir/adicionar/', ProdutoCriarView.as_view(), name='adicionar_produto'),
    path('produtos/gerir/editar/<slug:slug>/', ProdutoEditarView.as_view(), name='editar_produto'),

    # Carrinho
    path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('carrinho/item/adicionar/<slug:produto_slug>/', AdicionarAoCarrinhoView.as_view(), name='adicionar_carrinho'),
    path('carrinho/item/remover/<slug:produto_slug>/', RemoverDoCarrinhoView.as_view(), name='remover_carrinho'),
    path('carrinho/checkout/', FinalizarCompraView.as_view(), name='checkout'),

    # Perfil e Conta
    path('conta/perfil/', include([
        path('', PerfilView.as_view(), name='perfil'),
        path('configuracoes/', ConfiguracoesContaView.as_view(), name='configuracoes_conta'),
    ])),
    path('dashboard/', DashboardProdutorView.as_view(), name='dashboard'),

    # Páginas Institucionais
    path('sobre-nos/', SobreView.as_view(), name='quem_somos'),
    path('como-funciona/', ComoFuncionaView.as_view(), name='como_funciona'),
    path('politica-privacidade/', PoliticaPrivacidadeView.as_view(), name='politica_privacidade'),
    path('contactos/', ContactosView.as_view(), name='fala_connosco'),

    # Legal
    path('legal/termos-servico/', TemplateView.as_view(
        template_name='pt/institucional/termos_servico.html'
    ), name='termos_servico'),
    path('legal/politica-cookies/', TemplateView.as_view(
        template_name='pt/institucional/politica_cookies.html'
    ), name='politica_cookies'),
]
