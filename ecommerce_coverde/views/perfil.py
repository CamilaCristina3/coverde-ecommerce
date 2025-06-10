from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from ..models import  Produto, Pedido, Carrinho
from ..forms import PerfilUpdateForm, ProdutoForm

class PerfilView(LoginRequiredMixin, View):
    template_name = 'perfil/perfil.html'

    def get(self, request):
        user = request.user
        form = PerfilUpdateForm(instance=user)
        
        context = {
            'form': form,
            'user': user
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        form = PerfilUpdateForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
        
        context = {
            'form': form,
            'user': user
        }
        return render(request, self.template_name, context)


class ProdutorDashboardView(LoginRequiredMixin, View):
    template_name = 'perfil/produtor_dashboard.html'

    def get(self, request):
        if request.user.tipo != 'P':
            return redirect('perfil')
        
        produtos = Produto.objects.filter(produtor=request.user)
        pedidos = Pedido.objects.filter(
            itens__produto__produtor=request.user
        ).distinct().order_by('-data')[:10]
        
        context = {
            'produtos': produtos,
            'pedidos': pedidos,
            'total_produtos': produtos.count(),
            'pedidos_pendentes': pedidos.filter(status='P').count()
        }
        return render(request, self.template_name, context)


class ConsumidorDashboardView(LoginRequiredMixin, View):
    template_name = 'perfil/consumidor_dashboard.html'

    def get(self, request):
        if request.user.tipo != 'C':
            return redirect('perfil')
        
        pedidos = Pedido.objects.filter(consumidor=request.user).order_by('-data')
        carrinho, created = Carrinho.objects.get_or_create(utilizador=request.user)
        
        context = {
            'pedidos': pedidos[:5],
            'total_pedidos': pedidos.count(),
            'itens_carrinho': carrinho.itens.count()
        }
        return render(request, self.template_name, context)


class AdicionarProdutoView(LoginRequiredMixin, View):
    template_name = 'perfil/adicionar_produto.html'

    def get(self, request):
        if request.user.tipo != 'P':
            return redirect('perfil')
        
        form = ProdutoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.tipo != 'P':
            return redirect('perfil')
        
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.produtor = request.user
            produto.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('produtor_dashboard')
        
        return render(request, self.template_name, {'form': form})


class EditarProdutoView(LoginRequiredMixin, View):
    template_name = 'perfil/editar_produto.html'

    def get(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id, produtor=request.user)
        form = ProdutoForm(instance=produto)
        return render(request, self.template_name, {'form': form, 'produto': produto})

    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id, produtor=request.user)
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtor_dashboard')
        
        return render(request, self.template_name, {'form': form, 'produto': produto})