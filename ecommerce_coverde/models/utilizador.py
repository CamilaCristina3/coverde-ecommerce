from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import RegexValidator
import os
from uuid import uuid4


def user_directory_path(instance, filename):
    """Returns the path for profile image uploads with UUID to avoid collisions"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f'utilizadores/{instance.id}/{filename}'


def product_image_upload_path(instance, filename):
    """Generates a unique path to store product images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    product_name = slugify(instance.nome)
    return os.path.join('produtos', product_name, filename)


class UtilizadorManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password"""
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


class Utilizador(AbstractUser):
    class TipoUtilizador(models.TextChoices):
        CONSUMIDOR = 'C', _('Consumidor')
        PRODUTOR = 'P', _('Produtor')
        ADMIN = 'A', _('Administrador')

    # Removendo username e usando email como identificador único
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('Já existe uma conta com este email.')
        }
    )

    # Campos personalizados
    tipo = models.CharField(
        max_length=1,
        choices=TipoUtilizador.choices,
        default=TipoUtilizador.CONSUMIDOR,
        verbose_name=_('Tipo de Utilizador')
    )
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
    morada = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Morada')
    )
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
    imagem_perfil = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name=_('Imagem de Perfil'),
        help_text=_('Imagem de perfil do utilizador')
    )
    data_registo = models.DateTimeField(
        _('date joined'),
        auto_now_add=True,
        db_column='data_registo'  # Nome personalizado para o banco de dados
    )

    # Configuração de autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UtilizadorManager()

    # Related names personalizados para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="ecommerce_utilizador_set",
        related_query_name="ecommerce_utilizador",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="ecommerce_utilizador_set",
        related_query_name="ecommerce_utilizador",
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def clean(self):
        """Validação adicional do modelo"""
        super().clean()
        if self.nif:
            self.nif = self.nif.strip()
        if self.telefone:
            self.telefone = self.telefone.strip()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    # Métodos de negócio
    def get_produtos(self):
        """Retorna os produtos do produtor"""
        if hasattr(self, 'produtos'):
            return self.produtos.all()
        return None

    def get_pedidos(self):
        """Retorna os pedidos do consumidor"""
        if hasattr(self, 'pedidos'):
            return self.pedidos.all().order_by('-data')
        return None

    def get_total_gasto(self):
        """Calcula o total gasto pelo consumidor"""
        if hasattr(self, 'pedidos'):
            return sum(pedido.total for pedido in self.pedidos.all() if pedido.total)
        return 0

    def get_total_vendas(self):
        """Calcula o total de vendas do produtor"""
        if hasattr(self, 'produtos'):
            return sum(
                item.pedido.total 
                for produto in self.produtos.all() 
                for item in produto.itens_pedido.all()
                if item.pedido and item.pedido.total
            )
        return 0

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