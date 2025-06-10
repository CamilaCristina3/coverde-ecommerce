import random
import os
from django.conf import settings
from django.shortcuts import render
from django.views import View
from ..models import Produto, Categoria  # Removido Utilizador, pois não é necessário aqui

class Index(View):
    def get(self, request):
        """Método para lidar com requisições GET"""
        produtos = Produto.objects.filter(disponivel=True)
        return render(request, 'ecommerce_coverde/core/index.html', {'produtos': produtos})
        
        # ✅ Obter categorias (limite de 8)
        categorias = Categoria.objects.all()[:8]
        
        # ✅ Filtrar produtos por categoria, se aplicável
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            produtos = Produto.objects.filter(
                categoria__id=categoria_id,
                disponivel=True
            )
        else:
            # ✅ Produtos em destaque (prioridade)
            produtos_destaque = Produto.objects.filter(
                destaque=True,
                disponivel=True
            ).order_by('-data_criacao')[:4]
            
            # ✅ Outros produtos aleatórios
            outros_produtos = Produto.objects.filter(
                disponivel=True
            ).exclude(
                id__in=[p.id for p in produtos_destaque]
            ).order_by('?')[:8]  # 8 produtos aleatórios
            
            # ✅ Misturar os produtos
            produtos = list(produtos_destaque) + list(outros_produtos)
            random.shuffle(produtos)

        # ✅ Selecionar imagem de capa aleatória
        covers_folder = os.path.join(settings.BASE_DIR, 'static', 'imgs', 'covers')
        try:
            all_images = [
                f for f in os.listdir(covers_folder) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]
            selected_image = random.choice(all_images) if all_images else 'default-cover.jpg'
        except FileNotFoundError:
            selected_image = 'default-cover.jpg'
            
        selected_image_url = f'imgs/covers/{selected_image}'

        # ✅ Contexto para o template
        context = {
            "categorias": categorias,
            "produtos": produtos,
            "cover_image": selected_image_url,
            "user": request.user  # O Django já fornece o usuário autenticado
        }
        
        return render(request, "index.html", context)
