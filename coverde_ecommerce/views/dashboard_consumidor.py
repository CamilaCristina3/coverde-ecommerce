from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from coverde_ecommerce.models import Carrinho, Pedido, Produto

class ConsumidorDashboardView(LoginRequiredMixin, View):
    template_name = 'perfil/dasboard_consumidor.html'

    def get(self, request):
        if request.user.tipo != 'C':
            return redirect('coverde_ecommerce:perfil')

        # Buscar os pedidos do consumidor
        pedidos = Pedido.objects.filter(utilizador=request.user).order_by('-data_criacao')
        
        # Carrinho do consumidor (cria se não existir)
        carrinho, _ = Carrinho.objects.get_or_create(utilizador=request.user)

        # Exemplo de recomendação simples: últimos produtos disponíveis
        produtos_recomendados = Produto.objects.filter(disponivel=True).order_by('-data_criacao')[:6]

        context = {
            'pedidos_recentes': pedidos[:5],
            'total_pedidos': pedidos.count(),
            'itens_carrinho': carrinho.itens.count(),
            'produtos_recomendados': produtos_recomendados
        }
        return render(request, self.template_name, context)
