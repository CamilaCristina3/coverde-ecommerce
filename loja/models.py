from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.text import slugify


# -------------------------
# Gestão de utilizadores
# -------------------------

class UtilizadorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O email é obrigatório'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Utilizador(AbstractUser):
    class TipoUtilizador(models.TextChoices):
        CONSUMIDOR = 'C', _('Consumidor')
        PRODUTOR = 'P', _('Produtor')
        ADMIN = 'A', _('Administrador')

    username = None
    email = models.EmailField(_('email address'), unique=True)

    tipo = models.CharField(
        max_length=1,
        choices=TipoUtilizador.choices,
        default=TipoUtilizador.CONSUMIDOR,
        verbose_name=_('Tipo de Utilizador')
    )
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Telefone'))
    nif = models.CharField(max_length=9, blank=True, null=True, unique=True, verbose_name=_('NIF'))
    morada = models.TextField(blank=True, null=True, verbose_name=_('Morada'))
    codigo_postal = models.CharField(max_length=8, blank=True, null=True, verbose_name=_('Código Postal'))
    localidade = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Localidade'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UtilizadorManager()

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        verbose_name = _('Utilizador')
        verbose_name_plural = _('Utilizadores')
        ordering = ['-date_joined']


# -------------------------
# Categorias de produto
# -------------------------

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name=_('Nome'))
    descricao = models.TextField(blank=True, verbose_name=_('Descrição'))
    icone = models.CharField(max_length=30, default='fa-leaf', verbose_name=_('Ícone'))
    ordem_menu = models.PositiveSmallIntegerField(default=0, verbose_name=_('Ordem no Menu'))

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['ordem_menu', 'nome']


# -------------------------
# Produtos
# -------------------------

class Produto(models.Model):
    class UnidadeMedida(models.TextChoices):
        KILO = 'kg', _('Quilograma')
        GRAMA = 'g', _('Grama')
        UNIDADE = 'un', _('Unidade')
        LITRO = 'lt', _('Litro')
        DUZIA = 'dz', _('Dúzia')

    produtor = models.ForeignKey(
        Utilizador,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'P'},
        related_name='produtos',
        verbose_name=_('Produtor')
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='produtos',
        verbose_name=_('Categoria')
    )
    nome = models.CharField(max_length=100, verbose_name=_('Nome do Produto'))
    slug = models.SlugField(unique=True, max_length=120, verbose_name=_('Slug do Produto'))
    descricao = models.TextField(verbose_name=_('Descrição'))
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_('Preço Unitário')
    )
    unidade = models.CharField(
        max_length=2,
        choices=UnidadeMedida.choices,
        verbose_name=_('Unidade de Medida')
    )
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock Disponível'))
    imagem = models.ImageField(upload_to='produtos/', verbose_name=_('Imagem do Produto'))
    data_colheita = models.DateField(verbose_name=_('Data de Colheita/Produção'))
    certificado_biologico = models.BooleanField(default=False, verbose_name=_('Produto Biológico'))
    disponivel = models.BooleanField(default=True, verbose_name=_('Disponível para Venda'))
    destaque = models.BooleanField(default=False, verbose_name=_('Produto em Destaque'))
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Criação'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.produtor.get_short_name()}"

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['-destaque', '-data_criacao']
        indexes = [
            models.Index(fields=['disponivel', 'destaque']),
            models.Index(fields=['categoria', 'disponivel']),
        ]


# -------------------------
# Encomendas
# -------------------------

class Encomenda(models.Model):
    class EstadoEncomenda(models.TextChoices):
        PENDENTE = 'P', _('Pendente')
        PROCESSAMENTO = 'R', _('Em Processamento')
        ENVIADA = 'E', _('Enviada')
        ENTREGUE = 'D', _('Entregue')
        CANCELADA = 'C', _('Cancelada')

    consumidor = models.ForeignKey(
        Utilizador,
        on_delete=models.PROTECT,
        limit_choices_to={'tipo': 'C'},
        related_name='encomendas',
        verbose_name=_('Consumidor')
    )
    data = models.DateTimeField(auto_now_add=True, verbose_name=_('Data da Encomenda'))
    estado = models.CharField(
        max_length=1,
        choices=EstadoEncomenda.choices,
        default=EstadoEncomenda.PENDENTE,
        verbose_name=_('Estado')
    )
    observacoes = models.TextField(blank=True, verbose_name=_('Observações'))

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    class Meta:
        verbose_name = _('Encomenda')
        verbose_name_plural = _('Encomendas')
        ordering = ['-data']
        permissions = [
            ('mudar_estado_encomenda', 'Pode alterar estado da encomenda'),
        ]


# -------------------------
# Itens de Encomenda
# -------------------------

class ItemEncomenda(models.Model):
    encomenda = models.ForeignKey(
        Encomenda,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name=_('Encomenda')
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name=_('Produto')
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('Quantidade')
    )
    preco_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Preço Unitário')
    )

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    class Meta:
        verbose_name = _('Item de Encomenda')
        verbose_name_plural = _('Itens de Encomenda')
