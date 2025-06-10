from django.db import models
from django.conf import settings
from ecommerce_coverde.models.produto import Produto  # Corrigido conforme sua estrutura
import uuid

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
    endereco_entrega = models.TextField(
        verbose_name='Endereço de Entrega'
    )
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

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} para {self.pedido}"


class Carrinho(models.Model):
    utilizador = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrinho'
    )
    atualizado_em = models.DateTimeField(auto_now=True)

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

    @property
    def subtotal(self):
        return self.quantidade * self.preco

    class Meta:
        unique_together = ('carrinho', 'produto')
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no carrinho"
