# Generated by Django 5.2.1 on 2025-05-18 07:44

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('icone', models.CharField(default='fa-leaf', max_length=30, verbose_name='Ícone')),
                ('ordem_menu', models.PositiveSmallIntegerField(default=0, verbose_name='Ordem no Menu')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['ordem_menu', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('tipo', models.CharField(choices=[('C', 'Consumidor'), ('P', 'Produtor'), ('A', 'Administrador')], default='C', max_length=1, verbose_name='Tipo de Utilizador')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone')),
                ('nif', models.CharField(blank=True, max_length=9, null=True, unique=True, verbose_name='NIF')),
                ('morada', models.TextField(blank=True, null=True, verbose_name='Morada')),
                ('codigo_postal', models.CharField(blank=True, max_length=8, null=True, verbose_name='Código Postal')),
                ('localidade', models.CharField(blank=True, max_length=100, null=True, verbose_name='Localidade')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilizador',
                'verbose_name_plural': 'Utilizadores',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('utilizador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho', to=settings.AUTH_USER_MODEL, verbose_name='Utilizador')),
            ],
            options={
                'verbose_name': 'Carrinho',
                'verbose_name_plural': 'Carrinhos',
            },
        ),
        migrations.CreateModel(
            name='Encomenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da Encomenda')),
                ('estado', models.CharField(choices=[('P', 'Pendente'), ('R', 'Em Processamento'), ('E', 'Enviada'), ('D', 'Entregue'), ('C', 'Cancelada')], default='P', max_length=1, verbose_name='Estado')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('consumidor', models.ForeignKey(limit_choices_to={'tipo': 'C'}, on_delete=django.db.models.deletion.PROTECT, related_name='encomendas', to=settings.AUTH_USER_MODEL, verbose_name='Consumidor')),
            ],
            options={
                'verbose_name': 'Encomenda',
                'verbose_name_plural': 'Encomendas',
                'ordering': ['-data'],
                'permissions': [('mudar_estado_encomenda', 'Pode alterar estado da encomenda')],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Produto')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='Slug do Produto')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Preço Unitário')),
                ('unidade', models.CharField(choices=[('kg', 'Quilograma'), ('g', 'Grama'), ('un', 'Unidade'), ('lt', 'Litro'), ('dz', 'Dúzia')], max_length=2, verbose_name='Unidade de Medida')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock Disponível')),
                ('imagem', models.ImageField(upload_to='produtos/', verbose_name='Imagem do Produto')),
                ('data_colheita', models.DateField(verbose_name='Data de Colheita/Produção')),
                ('certificado_biologico', models.BooleanField(default=False, verbose_name='Produto Biológico')),
                ('disponivel', models.BooleanField(default=True, verbose_name='Disponível para Venda')),
                ('destaque', models.BooleanField(default=False, verbose_name='Produto em Destaque')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='loja.categoria', verbose_name='Categoria')),
                ('produtor', models.ForeignKey(limit_choices_to={'tipo': 'P'}, on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to=settings.AUTH_USER_MODEL, verbose_name='Produtor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['-destaque', '-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='ItemEncomenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantidade')),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço Unitário')),
                ('encomenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='loja.encomenda', verbose_name='Encomenda')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loja.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item de Encomenda',
                'verbose_name_plural': 'Itens de Encomenda',
            },
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantidade')),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='loja.carrinho', verbose_name='Carrinho')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item no Carrinho',
                'verbose_name_plural': 'Itens no Carrinho',
            },
        ),
        migrations.AddIndex(
            model_name='produto',
            index=models.Index(fields=['disponivel', 'destaque'], name='loja_produt_disponi_9dc21c_idx'),
        ),
        migrations.AddIndex(
            model_name='produto',
            index=models.Index(fields=['categoria', 'disponivel'], name='loja_produt_categor_18f98a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='itemcarrinho',
            unique_together={('carrinho', 'produto')},
        ),
    ]
