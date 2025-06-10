import os
import unicodedata
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from ecommerce_coverde.models.utilizador import Utilizador
from ecommerce_coverde.models.categoria import Categoria


def product_image_upload_path(instance, filename):
    """Gera caminho único para upload de imagens seguindo estrutura: produtos/<slug-produto>/<uuid>.<ext>"""
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('produtos', instance.slug or 'temp', filename)

class Produto(models.Model):
    class UnidadeMedida(models.TextChoices):
        KG = 'kg', _('Quilograma')
        G = 'g', _('Grama')
        UN = 'un', _('Unidade')
        L = 'l', _('Litro')
        ML = 'ml', _('Mililitro')
        CX = 'cx', _('Caixa')
        FD = 'fd', _('Fardo')

    # Informações Básicas
    nome = models.CharField(
        max_length=100,
        verbose_name=_('Nome do Produto'),
        help_text=_('Nome completo do produto para exibição')
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name=_('URL Amigável'),
        help_text=_('Gerado automaticamente a partir do nome')
    )
    
    descricao = models.TextField(
        verbose_name=_('Descrição Detalhada'),
        blank=True,
        help_text=_('Informações técnicas e características do produto')
    )
    
    # Dados Comerciais
    preco = models.DecimalField(
        max_digits=10,  # Aumentado para valores maiores
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_('Preço Unitário (€)')
    )
    
    unidade = models.CharField(
        max_length=2,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UN,
        verbose_name=_('Unidade de Venda')
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantidade em Stock'),
        help_text=_('Quantidade disponível para venda imediata')
    )
    
    # Imagens e Mídia
    imagem = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name=_('Imagem Principal'),
        blank=True,
        null=True,
        help_text=_('Imagem de destaque do produto (ratio recomendado 1:1)')
    )
    
    # Informações de Produção
    data_colheita = models.DateField(
        verbose_name=_('Data de Colheita/Produção'),
        blank=True,
        null=True,
        help_text=_('Data aproximada de produção do item')
    )
    
    certificado_biologico = models.BooleanField(
        default=False,
        verbose_name=_('Certificação Biológica'),
        help_text=_('Produto possui certificação orgânica/biológica?')
    )
    
    # Status e Disponibilidade
    disponivel = models.BooleanField(
        default=True,
        verbose_name=_('Disponível para Venda'),
        help_text=_('Exibir este produto no catálogo?')
    )
    
    destaque = models.BooleanField(
        default=False,
        verbose_name=_('Produto em Destaque'),
        help_text=_('Exibir em seções especiais do site')
    )
    
    # Metadados
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data de Cadastro')
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Última Atualização')
    )
    
    # Relacionamentos
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
        verbose_name=_('Categoria Principal')
    )
    
    produtor = models.ForeignKey(
        Utilizador,
        on_delete=models.PROTECT,  # Evita deletar produtor com produtos ativos
        limit_choices_to={'tipo': Utilizador.TipoUtilizador.PRODUTOR},
        related_name='produtos_cadastrados',
        verbose_name=_('Produtor/Fornecedor')
    )

    # Gerenciamento de Slug
    def generate_slug(self):
        """Gera slug ASCII-friendly com tratamento para duplicatas"""
        if not self.nome:
            return f"produto-{self.id or uuid4().hex[:8]}"  
        nome_ascii = unicodedata.normalize('NFKD', self.nome)
        nome_ascii = nome_ascii.encode('ascii', 'ignore').decode('ascii')
        base_slug = slugify(nome_ascii)[:100]  # Limita tamanho
        
        if not base_slug:
            base_slug = f"produto-{self.id or uuid4().hex[:8]}"
            
        slug = base_slug
        counter = 1
        
        while Produto.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug

    def save(self, *args, **kwargs):
        """Atualiza slug e garante integridade antes de salvar"""
        if not self.slug or self.slug.startswith('temp'):
            self.slug = self.generate_slug()
            
        # Garante que produtos indisponíveis não sejam destacados
        if not self.disponivel:
            self.destaque = False
            
        super().save(*args, **kwargs)
        
        # Atualiza caminho da imagem se slug mudou
        if self.imagem and ('temp' in self.imagem.name or not self.imagem.name.startswith(f'produtos/{self.slug}')):
            old_path = self.imagem.path
            new_name = product_image_upload_path(self, os.path.basename(self.imagem.name))

          # Cria o diretório se não existir
            os.makedirs(os.path.dirname(new_name), exist_ok=True)

    # Métodos de Negócio
    def em_estoque(self):
        """Verifica disponibilidade imediata"""
        return self.stock > 0 and self.disponivel
    
    def preco_promocional(self, desconto=0):
        """Calcula preço com desconto aplicado"""
        return round(self.preco * (1 - desconto/100), 2)

    # Representações
    def __str__(self):
        return f"{self.nome} ({self.get_unidade_display()}) - {self.produtor.get_short_name()}"

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['-destaque', '-data_criacao']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['disponivel', 'destaque']),
            models.Index(fields=['categoria', 'disponivel']),
            models.Index(fields=['preco']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_produto_slug'
            ),
            models.CheckConstraint(
                check=models.Q(preco__gte=0.01),
                name='preco_positivo'
            )
        ]