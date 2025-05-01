from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def user_directory_path(instance, filename):
    return f'uploads/profiles/{instance.id}/{filename}'


def product_image_upload_path(instance, filename):
    return f"uploads/products/{instance.produto.id}/{filename}"


# === GERENCIADOR DE USUÁRIOS PERSONALIZADOS ===
class UserManager(BaseUserManager):
    def create_user(self, email, primeiro_nome, ultimo_nome, telemovel, password=None, perfil='consumidor'):
        if not email:
            raise ValueError("O email é obrigatório!")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telemovel=telemovel,
            perfil=perfil
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primeiro_nome, ultimo_nome, telemovel, password=None):
        user = self.create_user(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telemovel=telemovel,
            password=password,
            perfil='produtor'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# === CATEGORIA ===
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='uploads/categorias/', blank=True, null=True)

    def __str__(self):
        return self.nome


# === USUÁRIO PERSONALIZADO ===
class User(AbstractBaseUser, PermissionsMixin):
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    telemovel = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    perfil = models.CharField(
        max_length=10,
        choices=[('consumidor', 'Consumidor'), ('produtor', 'Produtor')],
        default='consumidor'
    )
    localidade = models.CharField(max_length=100, blank=True, null=True)  # já existente
    cidade = models.CharField(max_length=100, blank=True, null=True)      
    descricao = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    categorias_produzidas = models.ManyToManyField(Categoria, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["primeiro_nome", "ultimo_nome", "telemovel"]

    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"


# === PRODUTO ===
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    quantidade = models.CharField(max_length=50)  # ex: "1kg", "caixa 5kg"
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    produtor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'perfil': 'produtor'})
    descricao = models.TextField(blank=True, null=True)
    data_colheita = models.DateField(blank=True, null=True)
    modo_producao = models.CharField(
        max_length=20,
        choices=[
            ('convencional', 'Convencional'),
            ('biologico', 'Biológico'),
            ('hidroponico', 'Hidropónico'),
        ],
        default='convencional'
    )

    def __str__(self):
        return f"{self.nome} - {self.quantidade}"

    class Meta:
        ordering = ['nome']


# === IMAGENS DOS PRODUTOS ===
class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name="imagens", on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return f"Imagem de {self.produto.nome}"


# === CONTACTOS ===
class MensagemDeContacto(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.nome}"

    class Meta:
        verbose_name = "Mensagem de Contacto"
        verbose_name_plural = "Mensagens de Contacto"
        ordering = ['-data_envio']


class Pedido(models.Model):
    consumidor = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.consumidor.email}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario