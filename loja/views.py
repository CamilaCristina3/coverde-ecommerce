from django.shortcuts import render, redirect, get_object_or_404  # 'render' adicionado aqui
from django.views.generic import (
    View, ListView, DetailView, CreateView, 
    TemplateView, FormView, UpdateView
)
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Produto, Categoria, Carrinho, ItemCarrinho
from .forms import (
    ConsumidorSignupForm, 
    ProdutorSignupForm,
    ProdutoForm,
    CheckoutForm
)

class IndexView(View):
    template_name = 'pt/index.html'

    def get(self, request):
        produtos_destaque = Produto.objects.filter(
            disponivel=True, 
            destaque=True
        )[:8]
        categorias = Categoria.objects.all()[:6]
        
        context = {
            'produtos_destaque': produtos_destaque,
            'categorias': categorias
        }
        return render(request, self.template_name, context)

# Autenticação
class CustomLoginView(LoginView):
    template_name = 'pt/auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.tipo == 'P':
            return reverse_lazy('loja:dashboard')
        return reverse_lazy('loja:index')

class SignupConsumidorView(CreateView):
    form_class = ConsumidorSignupForm
    template_name = 'pt/auth/signup_consumidor.html'
    success_url = reverse_lazy('loja:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta de consumidor criada com sucesso!')
        return response

class SignupProdutorView(CreateView):
    form_class = ProdutorSignupForm
    template_name = 'pt/auth/signup_produtor.html'
    success_url = reverse_lazy('loja:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta de produtor criada com sucesso!')
        return response

# Produtos
class ProdutoListView(ListView):
    model = Produto
    template_name = 'pt/produtos/listagem.html'
    paginate_by = 12
    context_object_name = 'produtos'

    def get_queryset(self):
        queryset = super().get_queryset().filter(disponivel=True)
        
        # Filtro por categoria
        if 'categoria' in self.request.GET:
            queryset = queryset.filter(categoria__slug=self.request.GET['categoria'])
        
        # Pesquisa
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            queryset = queryset.filter(
                Q(nome__icontains=query) | 
                Q(descricao__icontains=query)
            )
        
        return queryset

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'pt/produtos/detalhe.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.tipo == 'C':
            context['no_carrinho'] = ItemCarrinho.objects.filter(
                carrinho__consumidor=self.request.user,
                produto=self.object
            ).exists()
        return context

class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'pt/produtos/form_produto.html'
    success_url = reverse_lazy('loja:meus_produtos')

    def test_func(self):
        return self.request.user.tipo == 'P'

    def form_valid(self, form):
        form.instance.produtor = self.request.user
        messages.success(self.request, 'Produto adicionado com sucesso!')
        return super().form_valid(form)

# Carrinho
class CarrinhoView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'pt/carrinho/index.html'

    def test_func(self):
        return self.request.user.tipo == 'C'

    def get(self, request):
        carrinho, created = Carrinho.objects.get_or_create(consumidor=request.user)
        return render(request, self.template_name, {'carrinho': carrinho})

class AdicionarAoCarrinhoView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.tipo == 'C'

    def post(self, request, slug):
        produto = get_object_or_404(Produto, slug=slug, disponivel=True)
        carrinho, created = Carrinho.objects.get_or_create(consumidor=request.user)
        
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            defaults={'preco_unitario': produto.preco}
        )
        
        if not created:
            item.quantidade += 1
            item.save()
        
        messages.success(request, 'Produto adicionado ao carrinho!')
        return redirect('loja:carrinho')

class CheckoutView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'pt/carrinho/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('loja:checkout_sucesso')

    def test_func(self):
        return self.request.user.tipo == 'C'

    def form_valid(self, form):
        # Processar pagamento aqui (simulação)
        carrinho = get_object_or_404(Carrinho, consumidor=self.request.user)
        carrinho.itens.all().delete()
        messages.success(self.request, 'Compra realizada com sucesso!')
        return super().form_valid(form)

# Institucional
class SobreView(TemplateView):
    template_name = 'pt/institucional/sobre.html'

class ContactosView(TemplateView):
    template_name = 'pt/institucional/contactos.html'

class NovidadesView(ListView):
    template_name = 'pt/institucional/novidades.html'
    queryset = Produto.objects.filter(disponivel=True).order_by('-data_criacao')[:6]
    context_object_name = 'novidades'