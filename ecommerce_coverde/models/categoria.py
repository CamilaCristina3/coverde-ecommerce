from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, RegexValidator

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
        blank=True,  # Mudado de null=True para blank=True
        verbose_name=_('Slug'),
        help_text=_('Identificador único para URLs (gerado automaticamente)')
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
        help_text=_('Ordem de exibição no menu (menor aparece primeiro)')
    )

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        
        # Garante que o slug seja único
        original_slug = self.slug
        counter = 1
        
        while Categoria.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['ordem_menu', 'nome']
        db_table = 'ecommerce_coverde_categoria'
        indexes = [
            models.Index(fields=['slug'], name='categoria_slug_idx'),
            models.Index(fields=['ordem_menu'], name='categoria_ordem_idx'),
        ]