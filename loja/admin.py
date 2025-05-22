from django.contrib import admin
from loja.models import Utilizador, Categoria, Produto, Encomenda, ItemEncomenda
from django.utils.translation import gettext_lazy as _


@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'tipo', 'is_active', 'is_staff')
    list_filter = ('tipo', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (_('Informações Pessoais'), {
            'fields': ('email', 'first_name', 'last_name', 'tipo', 'nif', 'telefone', 'morada', 'codigo_postal', 'localidade')
        }),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'tipo')}
        ),
    )
    readonly_fields = ('last_login', 'date_joined')
    exclude = ('username',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem_menu', 'icone')
    search_fields = ('nome',)
    ordering = ('ordem_menu', 'nome')


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'produtor', 'preco', 'stock', 'disponivel', 'destaque')
    list_filter = ('categoria', 'disponivel', 'destaque', 'certificado_biologico')
    search_fields = ('nome', 'descricao', 'slug')
    prepopulated_fields = {'slug': ('nome',)}  # Preenche slug com base no nome (só na criação)
    readonly_fields = ('slug', 'data_criacao')
    fieldsets = (
        (None, {
            'fields': (
                'nome', 'slug', 'descricao', 'categoria', 'produtor', 'preco',
                'unidade', 'stock', 'imagem', 'data_colheita', 'certificado_biologico',
                'disponivel', 'destaque', 'data_criacao'
            )
        }),
    )


@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'consumidor', 'data', 'estado', 'total')
    list_filter = ('estado', 'data')
    search_fields = ('consumidor__email', 'id')
    readonly_fields = ('data',)


@admin.register(ItemEncomenda)
class ItemEncomendaAdmin(admin.ModelAdmin):
    list_display = ('encomenda', 'produto', 'quantidade', 'preco_unitario', 'subtotal')
    search_fields = ('produto__nome',)
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return obj.subtotal()



