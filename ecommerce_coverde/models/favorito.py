from django.db import models
from django.conf import settings
from .produto import Produto

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

    def __str__(self):
        return f"{self.utilizador} ♥ {self.produto}"
