from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(max_length=200, default='Mensagem via formulário de contacto')
    mensagem = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nome} ({self.email}) - {self.assunto[:30]}"
