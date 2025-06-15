from django.shortcuts import redirect, render
from django.views import View
from backend.ecommerce_coverde.models.pedido import Carrinho, Pedido
from django.contrib.auth.mixins import LoginRequiredMixin , View


class ConsumidorDashboardView(LoginRequiredMixin, View):
    template_name = 'perfil/consumidor_dashboard.html'

    def get(self, request):
        if request.user.tipo != 'C':
            return redirect('ecommerce_coverde:perfil')
        
        pedidos = Pedido.objects.filter(utilizador=request.user).order_by('-data_criacao')
        carrinho, _ = Carrinho.objects.get_or_create(utilizador=request.user)
        
        context = {
            'pedidos': pedidos[:5],
            'total_pedidos': pedidos.count(),
            'itens_carrinho': carrinho.itens.count()
        }
        return render(request, self.template_name, context)
