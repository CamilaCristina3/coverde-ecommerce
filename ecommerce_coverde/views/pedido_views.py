from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from ..models import Pedido, ItemPedido, Carrinho
from ..forms import PedidoForm, CheckoutForm

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'ecommerce_coverde/pedido/list.html'
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-data_criacao')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'ecommerce_coverde/pedido/detail.html'
    context_object_name = 'pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)

class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'ecommerce_coverde/pedido/create.html'
    success_url = reverse_lazy('ecommerce_coverde:pedido-list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'ecommerce_coverde/pedido/update.html'
    context_object_name = 'pedido'
    
    def get_success_url(self):
        return reverse_lazy('ecommerce_coverde:pedido-detail', kwargs={'pk': self.object.pk})

class PedidoCancelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pedido = get_object_or_404(Pedido, pk=kwargs['pk'], usuario=request.user)
        pedido.status = 'cancelado'
        pedido.save()
        messages.success(request, 'Pedido cancelado com sucesso!')
        return redirect('ecommerce_coverde:pedido-list')

# Carrinho Views
class CarrinhoView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/carrinho.html'
    
    def get(self, request, *args, **kwargs):
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
        return render(request, self.template_name, {'carrinho': carrinho})

class AdicionarAoCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        produto_id = kwargs['produto_id']
        quantidade = request.POST.get('quantidade', 1)
        
        with transaction.atomic():
            carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
            carrinho.adicionar_item(produto_id, quantidade)
        
        messages.success(request, 'Produto adicionado ao carrinho!')
        return redirect('ecommerce_coverde:carrinho')

class RemoverDoCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        produto_id = kwargs['produto_id']
        
        with transaction.atomic():
            carrinho = get_object_or_404(Carrinho, usuario=request.user)
            carrinho.remover_item(produto_id)
        
        messages.success(request, 'Produto removido do carrinho!')
        return redirect('ecommerce_coverde:carrinho')

class LimparCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        carrinho.itens.all().delete()
        messages.success(request, 'Carrinho limpo com sucesso!')
        return redirect('ecommerce_coverde:carrinho')

# Checkout Views
class CheckoutView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/checkout.html'
    
    def get(self, request, *args, **kwargs):
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        if not carrinho.itens.exists():
            messages.warning(request, 'Seu carrinho está vazio!')
            return redirect('ecommerce_coverde:carrinho')
        
        form = CheckoutForm()
        return render(request, self.template_name, {'form': form, 'carrinho': carrinho})
    
    def post(self, request, *args, **kwargs):
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                pedido = form.save(commit=False)
                pedido.usuario = request.user
                pedido.save()
                
                for item in carrinho.itens.all():
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=item.produto,
                        quantidade=item.quantidade,
                        preco=item.produto.preco
                    )
                
                carrinho.itens.all().delete()
                return redirect('ecommerce_coverde:checkout-success', codigo=pedido.codigo)
        
        return render(request, self.template_name, {'form': form, 'carrinho': carrinho})

class CheckoutSuccessView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/checkout_success.html'
    
    def get(self, request, *args, **kwargs):
        codigo = kwargs['codigo']
        pedido = get_object_or_404(Pedido, codigo=codigo, usuario=request.user)
        return render(request, self.template_name, {'pedido': pedido})