from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from ecommerce_coverde.models import Pedido, ItemPedido, Carrinho
from ..forms import PedidoForm, CheckoutForm

# ======= PEDIDOS =======

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'ecommerce_coverde/pedido/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 10
    
    def get_queryset(self):
        # Removido select_related para endereco_entrega pois é TextField
        return Pedido.objects.filter(
            utilizador=self.request.user
        ).select_related('utilizador').prefetch_related('itens').order_by('-data_criacao')

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'ecommerce_coverde/pedido/pedido_detail.html'
    context_object_name = 'pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(utilizador=self.request.user)

class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'ecommerce_coverde/pedido/pedido_create.html'
    success_url = reverse_lazy('ecommerce_coverde:pedido_list')

    def form_valid(self, form):
        form.instance.utilizador = self.request.user
        return super().form_valid(form)

class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'ecommerce_coverde/pedido/pedido_update.html'
    context_object_name = 'pedido'
    
    def get_success_url(self):
        return reverse_lazy('ecommerce_coverde:pedido-detail', kwargs={'pk': self.object.pk})

class PedidoCancelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pedido = get_object_or_404(Pedido, pk=kwargs['pk'], utilizador=request.user)
        pedido.status = 'cancelado'
        pedido.save()
        messages.success(request, 'Pedido cancelado com sucesso!')
        return redirect('ecommerce_coverde:pedido_list')

# ======= CARRINHO =======

class CarrinhoView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/carrinho.html'

    def get(self, request, *args, **kwargs):
        carrinho, _ = Carrinho.objects.get_or_create(utilizador=request.user)
        return render(request, self.template_name, {'carrinho': carrinho})

class AdicionarAoCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        produto_id = kwargs['produto_id']
        quantidade = int(request.POST.get('quantidade', 1))

        with transaction.atomic():
            carrinho, _ = Carrinho.objects.get_or_create(utilizador=request.user)
            carrinho.adicionar_item(produto_id, quantidade)

        messages.success(request, 'Produto adicionado ao carrinho!')
        return redirect('ecommerce_coverde:carrinho')

class RemoverDoCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        produto_id = kwargs['produto_id']

        with transaction.atomic():
            carrinho = get_object_or_404(Carrinho, utilizador=request.user)
            carrinho.remover_item(produto_id)

        messages.success(request, 'Produto removido do carrinho!')
        return redirect('ecommerce_coverde:carrinho')

class LimparCarrinhoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrinho = get_object_or_404(Carrinho, utilizador=request.user)
        carrinho.itens.all().delete()
        messages.success(request, 'Carrinho limpo com sucesso!')
        return redirect('ecommerce_coverde:carrinho')

# ======= CHECKOUT =======

class CheckoutView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        self.carrinho = get_object_or_404(Carrinho, utilizador=request.user)
        if not self.carrinho.itens.exists():
            messages.warning(request, 'Seu carrinho está vazio!')
            return redirect('ecommerce_coverde:carrinho')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = CheckoutForm(initial={
            'endereco_entrega': request.user.morada if hasattr(request.user, 'morada') else '',
            'metodo_pagamento': 'cartao'
        })
        return render(request, self.template_name, {
            'form': form,
            'carrinho': self.carrinho
        })
    
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return self.processar_pedido(form, request)
        return render(request, self.template_name, {
            'form': form,
            'carrinho': self.carrinho
        })

    def processar_pedido(self, form, request):
        with transaction.atomic():
            pedido = form.save(commit=False)
            pedido.utilizador = request.user
            pedido.total = self.carrinho.total
            pedido.save()

            for item in self.carrinho.itens.all():
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item.produto,
                    quantidade=item.quantidade,
                    preco=item.produto.preco
                )

            self.carrinho.itens.all().delete()
            return redirect('ecommerce_coverde:checkout-success', codigo=pedido.codigo)

class CheckoutSuccessView(LoginRequiredMixin, View):
    template_name = 'ecommerce_coverde/pedido/checkout_success.html'

    def get(self, request, *args, **kwargs):
        codigo = kwargs['codigo']
        pedido = get_object_or_404(Pedido, codigo=codigo, utilizador=request.user)
        return render(request, self.template_name, {'pedido': pedido})
