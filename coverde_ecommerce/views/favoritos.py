from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from ..models import Favorito, Produto

class FavoritosListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = 'coverde_ecommerce/favoritos/favorito_list.html'  # <-- CORRETO
    context_object_name = 'favoritos'


    def get_queryset(self):
        return Favorito.objects.filter(utilizador=self.request.user).select_related('produto')

@login_required
def adicionar_favorito(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    favorito, created = Favorito.objects.get_or_create(
        usuario=request.user,
        produto=produto
    )
    if created:
        messages.success(request, f"'{produto.nome}' foi adicionado aos seus favoritos!")
    else:
        messages.info(request, f"'{produto.nome}' já está nos seus favoritos!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remover_favorito(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    Favorito.objects.filter(utilizador=request.user, produto=produto).delete()
    messages.success(request, f"'{produto.nome}' foi removido dos seus favoritos!")
    return redirect(request.META.get('HTTP_REFERER', 'favoritos'))