from django.db import models
from django.conf import settings

class Conversation(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversas_enviadas'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversas_recebidas'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user1', 'user2']]
        ordering = ['-created_at']
        verbose_name = 'Conversa'
        verbose_name_plural = 'Conversas'

    def __str__(self):
        return f"Conversa entre {self.user1.get_full_name()} e {self.user2.get_full_name()}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )
    text = models.TextField(verbose_name='Mensagem')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'

    def __str__(self):
        return f"Mensagem de {self.sender.get_short_name()} em {self.timestamp.strftime('%d/%m %H:%M')}"
