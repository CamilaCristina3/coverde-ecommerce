from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilizador, Produto, Categoria, Pedido, Carrinho, Favorito, ItemPedido, ItemCarrinho

# ========== CUSTOM USER ADMIN ==========
@admin.register(Utilizador)
class UtilizadorAdmin(UserAdmin):
    model = Utilizador
    list_display = ('email', 'first_name', 'last_name', 'tipo', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('tipo', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'nif')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
            'fields': (
                'first_name', 'last_name', 'tipo', 'telefone', 'nif',
                'morada', 'codigo_postal', 'localidade', 'imagem_perfil'
            )
        }),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'tipo',
                'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )
    readonly_fields = ('date_joined',)

# ========== PRODUTO ==========
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'produtor', 'preco', 'stock', 'disponivel', 'destaque')
    list_filter = ('disponivel', 'destaque', 'categoria')
    search_fields = ('nome', 'descricao', 'produtor__email')
    prepopulated_fields = {'slug': ('nome',)}

# ========== CATEGORIA ==========
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem_menu')
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ('ordem_menu',)

# ========== PEDIDO ==========
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'utilizador', 'status', 'total', 'data_criacao')
    list_filter = ('status',)
    search_fields = ('codigo', 'utilizador__email')
    inlines = [ItemPedidoInline]

# ========== CARRINHO ==========
class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('utilizador', 'atualizado_em')
    inlines = [ItemCarrinhoInline]

# ========== FAVORITO ==========
@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('utilizador', 'produto', 'criado_em')
    search_fields = ('utilizador__email', 'produto__nome')
