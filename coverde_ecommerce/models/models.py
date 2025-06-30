import os
import uuid
import unicodedata
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MinValueValidator
)

# ==================== UTILITÁRIOS ====================
def user_directory_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('utilizadores', str(instance.id), filename)

def product_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('produtos', instance.slug or 'temp', filename)

# ==================== GERENCIADOR ====================
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
        return self._create_user(email, password, **extra_fields)

# ==================== USUÁRIO PERSONALIZADO ====================
class Utilizador(AbstractUser):
    class TipoUtilizador(models.TextChoices):
        CONSUMIDOR = 'C', _('Consumidor')
        PRODUTOR = 'P', _('Produtor')
        ADMIN = 'A', _('Administrador')

    username = None
    email = models.EmailField(_('email address'), unique=True)
    tipo = models.CharField(max_length=1, choices=TipoUtilizador.choices, default=TipoUtilizador.CONSUMIDOR)

    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?[\d\s]{9,15}$', _('Formato de telefone inválido. Use +351 123456789'))]
    )
    nif = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        unique=True,
        validators=[RegexValidator(r'^\d{9}$', _('NIF deve conter exatamente 9 dígitos'))]
    )
    morada = models.TextField(blank=True, null=True)
    codigo_postal = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{4}-\d{3}$', _('Formato inválido. Use 1234-567'))]
    )
    localidade = models.CharField(max_length=100, blank=True, null=True)
    imagem_perfil = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    data_registo = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UtilizadorManager()

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def is_produtor(self):
        return self.tipo == self.TipoUtilizador.PRODUTOR

    def is_consumidor(self):
        return self.tipo == self.TipoUtilizador.CONSUMIDOR

    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'
        ordering = ['-data_registo']
        db_table = 'ecommerce_coverde_utilizadores'

# ==================== CATEGORIA ====================
class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=30, default='fa-leaf')
    ordem_menu = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            self.slug = base_slug
            counter = 1
            while Categoria.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['ordem_menu', 'nome']

# ==================== PRODUTO ====================
class Produto(models.Model):
    class UnidadeMedida(models.TextChoices):
        KG = 'kg', _('Quilograma')
        G = 'g', _('Grama')
        UN = 'un', _('Unidade')
        L = 'l', _('Litro')
        ML = 'ml', _('Mililitro')
        CX = 'cx', _('Caixa')
        FD = 'fd', _('Fardo')

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unidade = models.CharField(max_length=2, choices=UnidadeMedida.choices, default=UnidadeMedida.UN)
    stock = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    produtor = models.ForeignKey(Utilizador, on_delete=models.PROTECT, limit_choices_to={'tipo': Utilizador.TipoUtilizador.PRODUTOR})
    data_colheita = models.DateField(blank=True, null=True)
    certificado_biologico = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        if not self.disponivel:
            self.destaque = False
        super().save(*args, **kwargs)

    def generate_slug(self):
        nome_ascii = unicodedata.normalize('NFKD', self.nome).encode('ascii', 'ignore').decode('ascii')
        base_slug = slugify(nome_ascii)[:100] or f"produto-{uuid4().hex[:8]}"
        slug = base_slug
        counter = 1
        while Produto.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return f"{self.nome} ({self.get_unidade_display()})"

    class Meta:
        ordering = ['-destaque', '-data_criacao']

# ==================== PEDIDO ====================
class Pedido(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PAGO = 'pago', 'Pago'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGUE = 'entregue', 'Entregue'
        CANCELADO = 'cancelado', 'Cancelado'

    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    endereco_entrega = models.TextField()
    metodo_pagamento = models.CharField(max_length=50)

    def __str__(self):
        return f"Pedido #{self.codigo}"

    class Meta:
        ordering = ['-data_criacao']

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} para pedido {self.pedido.codigo}"

# ==================== CARRINHO ====================
class Carrinho(models.Model):
    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrinho')
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    def __str__(self):
        return f"Carrinho de {self.utilizador.get_full_name()}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

# ==================== FAVORITOS ====================
class Favorito(models.Model):
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='favoritos')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['utilizador', 'produto'], name='unique_favorito')
        ]

    def __str__(self):
        return f"{self.utilizador} ♥ {self.produto}"

# ==================== CONTACTO ====================
class ContactMessage(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(max_length=200, default='Mensagem via formulário de contacto')
    mensagem = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nome} ({self.email}) - {self.assunto[:30]}"

    class Meta:
        ordering = ['-data_envio']
        verbose_name = 'Mensagem de Contacto'
        verbose_name_plural = 'Mensagens de Contacto'
