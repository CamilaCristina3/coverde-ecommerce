import uuid
from django.db import models
from ..utils import user_directory_path
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MinValueValidator
)
from django.utils import timezone
import os
import unicodedata
from uuid import uuid4


# ==================== UTILITÁRIOS ====================
def user_directory_path(instance, filename):
    """Caminho para upload de imagens de perfil"""
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('utilizadores', str(instance.id), filename)


def product_image_upload_path(instance, filename):
    """Caminho para upload de imagens de produtos"""
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('produtos', instance.slug or 'temp', filename)


# ==================== GERENCIADORES ====================
class UtilizadorManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('O email é obrigatório'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo', Utilizador.TipoUtilizador.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


# ==================== MODELOS PRINCIPAIS ====================
class Utilizador(AbstractUser):
    class TipoUtilizador(models.TextChoices):
        CONSUMIDOR = 'C', _('Consumidor')
        PRODUTOR = 'P', _('Produtor')
        ADMIN = 'A', _('Administrador')

    # Campos base
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={'unique': _('Já existe uma conta com este email.')}
    )
    tipo = models.CharField(
        max_length=1,
        choices=TipoUtilizador.choices,
        default=TipoUtilizador.CONSUMIDOR,
        verbose_name=_('Tipo de Utilizador')
    )
    
    # Informações de contacto
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Telefone'),
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s]{9,15}$',
                message=_('Formato de telefone inválido. Use +351 123456789')
            )
        ]
    )
    
    # Informações fiscais
    nif = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('NIF'),
        validators=[
            RegexValidator(
                regex='^[0-9]{9}$',
                message=_('NIF deve conter exatamente 9 dígitos')
            )
        ]
    )
    
    # Morada
    morada = models.TextField(blank=True, null=True, verbose_name=_('Morada'))
    codigo_postal = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name=_('Código Postal'),
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{3}$',
                message=_('Formato inválido. Use 1234-567')
            )
        ]
    )
    localidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Localidade')
    )
    
    # Imagem e metadados
    imagem_perfil = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name=_('Imagem de Perfil')
    )
    data_registo = models.DateTimeField(
        _('date joined'),
        auto_now_add=True,
        db_column='data_registo'
    )

    # Configuração de autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UtilizadorManager()

    class Meta:
        verbose_name = _('Utilizador')
        verbose_name_plural = _('Utilizadores')
        ordering = ['-data_registo']
        db_table = 'ecommerce_coverde_utilizadores'
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['tipo'], name='tipo_utilizador_idx'),
            models.Index(fields=['nif'], name='nif_idx'),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class Categoria(models.Model):
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Nome'),
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex=r'^[\w\s-]+$',
                message=_('O nome deve conter apenas letras, números, espaços ou hífens')
            )
        ],
        help_text=_('Nome da categoria (mínimo 3 caracteres)')
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        verbose_name=_('Slug'),
        help_text=_('Identificador único para URLs')
    )
    descricao = models.TextField(
        blank=True,
        verbose_name=_('Descrição'),
        help_text=_('Descrição detalhada da categoria')
    )
    icone = models.CharField(
        max_length=30,
        default='fa-leaf',
        verbose_name=_('Ícone'),
        help_text=_('Classe do ícone (ex: Font Awesome)')
    )
    ordem_menu = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Ordem no Menu'),
        help_text=_('Ordem de exibição no menu')
    )

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['ordem_menu', 'nome']
        db_table = 'ecommerce_coverde_categoria'
        indexes = [
            models.Index(fields=['slug'], name='categoria_slug_idx'),
            models.Index(fields=['ordem_menu'], name='categoria_ordem_idx'),
        ]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        
        original_slug = self.slug
        counter = 1
        
        while Categoria.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        super().save(*args, **kwargs)


class Produto(models.Model):
    class UnidadeMedida(models.TextChoices):
        KG = 'kg', _('Quilograma')
        G = 'g', _('Grama')
        UN = 'un', _('Unidade')
        L = 'l', _('Litro')
        ML = 'ml', _('Mililitro')
        CX = 'cx', _('Caixa')
        FD = 'fd', _('Fardo')

    # Informações básicas
    nome = models.CharField(max_length=100, verbose_name=_('Nome do Produto'))
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name=_('URL Amigável')
    )
    descricao = models.TextField(
        verbose_name=_('Descrição Detalhada'),
        blank=True
    )
    
    # Dados comerciais
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_('Preço Unitário (€)')
    )

    # Dados de criação 
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
        
        )
    

    unidade = models.CharField(
        max_length=2,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UN,
        verbose_name=_('Unidade de Venda')
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantidade em Stock')
    )
    
    # Imagem
    imagem = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name=_('Imagem Principal'),
        blank=True,
        null=True
    )
    
    # Status
    disponivel = models.BooleanField(
        default=True,
        verbose_name=_('Disponível para Venda')
    )
    destaque = models.BooleanField(
        default=False,
        verbose_name=_('Produto em Destaque')
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
        on_delete=models.PROTECT,
        limit_choices_to={'tipo': Utilizador.TipoUtilizador.PRODUTOR},
        related_name='produtos_cadastrados',
        verbose_name=_('Produtor/Fornecedor')
    )


    data_colheita = models.DateField(
        verbose_name='Data de Colheita/Produção',
        blank=True,
        null=True,
        help_text='Data aproximada de colheita ou produção'
    )
    
    certificado_biologico = models.BooleanField(
        verbose_name='Certificação Biológica',
        default=False,
        help_text='Marque se o produto possui certificação orgânica/biológica'
    )

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

    def __str__(self):
        return f"{self.nome} ({self.get_unidade_display()}) - {self.produtor.get_short_name()}"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.startswith('temp'):
            self.slug = self.generate_slug()
            
        if not self.disponivel:
            self.destaque = False
            
        super().save(*args, **kwargs)
        
        if self.imagem and ('temp' in self.imagem.name or not self.imagem.name.startswith(f'produtos/{self.slug}')):
            self._move_uploaded_image()

    def _move_uploaded_image(self):
        """Move a imagem para o diretório correto se o slug mudou"""
        old_path = self.imagem.path
        new_name = product_image_upload_path(self, os.path.basename(self.imagem.name))
        os.makedirs(os.path.dirname(new_name), exist_ok=True)
        os.rename(old_path, new_name)
        self.imagem.name = new_name
        self.save(update_fields=['imagem'])

    def generate_slug(self):
        """Gera um slug único baseado no nome do produto"""
        if not self.nome:
            return f"produto-{self.id or uuid4().hex[:8]}"
            
        nome_ascii = unicodedata.normalize('NFKD', self.nome)
        nome_ascii = nome_ascii.encode('ascii', 'ignore').decode('ascii')
        base_slug = slugify(nome_ascii)[:100]
        
        if not base_slug:
            base_slug = f"produto-{self.id or uuid4().hex[:8]}"
            
        slug = base_slug
        counter = 1
        
        while Produto.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug

    def em_estoque(self):
        return self.stock > 0 and self.disponivel


# ==================== MODELOS DE PEDIDOS ====================
class Pedido(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PAGO = 'pago', 'Pago'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGUE = 'entregue', 'Entregue'
        CANCELADO = 'cancelado', 'Cancelado'


    codigo = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='Código do Pedido'
    )
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos',
        verbose_name='Cliente'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
        verbose_name='Estado do Pedido'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total (€)'
    )
    endereco_entrega = models.TextField(verbose_name='Endereço de Entrega')
    metodo_pagamento = models.CharField(
        max_length=50,
        verbose_name='Método de Pagamento'
    )

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.codigo}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} para {self.pedido}"


# ==================== MODELOS DE CARRINHO ====================
class Carrinho(models.Model):
    utilizador = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrinho'
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f"Carrinho de {self.utilizador.get_full_name()}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    def adicionar_item(self, produto_id, quantidade=1):
        produto = Produto.objects.get(pk=produto_id)
        item, created = self.itens.get_or_create(
            produto=produto,
            defaults={'quantidade': quantidade, 'preco': produto.preco}
        )
        if not created:
            item.quantidade += int(quantidade)
            item.save()

    def remover_item(self, produto_id):
        self.itens.filter(produto_id=produto_id).delete()


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho,
        related_name='itens',
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('carrinho', 'produto')
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no carrinho"


# ==================== MODELOS ADICIONAIS ====================
class ContactMessage(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(
        max_length=200,
        default='Mensagem via formulário de contacto'
    )
    mensagem = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Mensagem de Contacto'
        verbose_name_plural = 'Mensagens de Contacto'
        ordering = ['-data_envio']

    def __str__(self):
        return f"{self.nome} ({self.email}) - {self.assunto[:30]}"


class Favorito(models.Model):
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilizador', 'produto')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        db_table = 'ecommerce_coverde_favorito'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.utilizador} ♥ {self.produto}"