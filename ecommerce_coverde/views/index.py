import random
import os
from django.conf import settings
from django.shortcuts import render
from django.views import View
from ..models import Produto, Categoria
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'ecommerce_coverde/institucional/index.html'
    NUMBER_OF_CATEGORIES = 8
    NUMBER_OF_FEATURED_PRODUCTS = 4
    NUMBER_OF_RANDOM_PRODUCTS = 8
    
    def get_cover_image(self):
        """Obtém uma imagem de capa aleatória ou a padrão"""
        covers_folder = os.path.join(settings.BASE_DIR, 'static', 'imgs', 'covers')
        try:
            image_files = [
                f for f in os.listdir(covers_folder) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]
            selected_image = random.choice(image_files) if image_files else 'default-cover.jpg'
            return f'imgs/covers/{selected_image}'
        except (FileNotFoundError, OSError):
            return 'imgs/covers/default-cover.jpg'

    def get_filtered_products(self, categoria_id=None):
        """Obtém produtos filtrados por categoria ou a seleção padrão"""
        if categoria_id:
            return Produto.objects.filter(
                categoria__id=categoria_id,
                disponivel=True
            ).select_related('categoria')
        
        produtos_destaque = Produto.objects.filter(
            destaque=True,
            disponivel=True
        ).order_by('-data_criacao')[:self.NUMBER_OF_FEATURED_PRODUCTS]
        
        outros_produtos = Produto.objects.filter(
            disponivel=True
        ).exclude(
            id__in=[p.id for p in produtos_destaque]
        ).order_by('?')[:self.NUMBER_OF_RANDOM_PRODUCTS]
        
        product_list = list(produtos_destaque) + list(outros_produtos)
        random.shuffle(product_list)
        return product_list

    def get(self, request):
        """Método principal para lidar com requisições GET"""
        context = {
            "categorias": Categoria.objects.all()[:self.NUMBER_OF_CATEGORIES],
            "produtos": self.get_filtered_products(request.GET.get('categoria')),
            "cover_image": self.get_cover_image(),
            "user": request.user
        }
        # CORREÇÃO: Usando o mesmo caminho do template que você usou originalmente
        return render(request, "ecommerce_coverde/core/index.html", context)