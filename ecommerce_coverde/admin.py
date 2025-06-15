from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils.text import slugify

from .models import (
    Utilizador, Produto, Categoria, Pedido,
    ItemPedido, Carrinho, ItemCarrinho, Favorito, ContactMessage
)

class ProdutorFilter(admin.SimpleListFilter):
    title = 'Produtor'
    parameter_name = 'produtor'

    def lookups(self, request, model_admin):
        produtores = Utilizador.objects.filter(tipo=Utilizador.TipoUtilizador.PRODUTOR)
        return [(p.id, p.get_full_name()) for p in produtores]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(produtor__id=self.value())
        return queryset

@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'tipo', 'telefone', 'is_active', 'is_staff')
    list_filter = ('tipo', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'telefone', 'nif')
    readonly_fields = ('date_joined', 'last_login', 'imagem_perfil_preview')
    list_editable = ('is_active', 'is_staff')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informação Pessoal', {
            'fields': ('first_name', 'last_name', 'telefone', 'nif',
                       'imagem_perfil', 'imagem_perfil_preview')
        }),
        ('Localização', {
            'fields': ('morada', 'codigo_postal', 'localidade')
        }),
        ('Permissões', {
            'fields': ('tipo', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Nome Completo'
    full_name.admin_order_field = 'last_name'

    def imagem_perfil_preview(self, obj):
        if obj.imagem_perfil:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.imagem_perfil.url
            )
        return "-"
    imagem_perfil_preview.short_description = 'Preview'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'produtor_link', 'preco', 'unidade',
                    'stock', 'disponivel', 'destaque', 'certificado_biologico', 
                    'data_colheita', 'imagem_preview')
    list_filter = (ProdutorFilter, 'disponivel', 'destaque', 'categoria', 
                   'certificado_biologico', 'data_colheita')
    search_fields = ('nome', 'descricao', 'produtor__first_name', 'produtor__last_name')
    list_editable = ('preco', 'stock', 'disponivel', 'destaque', 'certificado_biologico')
    readonly_fields = ('data_criacao', 'imagem_preview', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    autocomplete_fields = ['produtor', 'categoria']
    date_hierarchy = 'data_criacao'
    actions = ['marcar_como_indisponivel', 'marcar_como_biologico']

    fieldsets = (
        (None, {
            'fields': ('nome', 'slug', 'descricao', 'produtor', 'categoria')
        }),
        ('Informações Comerciais', {
            'fields': ('preco', 'unidade', 'stock', 'disponivel', 'destaque')
        }),
        ('Certificações', {
            'fields': ('certificado_biologico', 'data_colheita')
        }),
        ('Imagem', {
            'fields': ('imagem', 'imagem_preview')
        }),
        ('Metadados', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('produtor', 'categoria')

    def produtor_link(self, obj):
        url = reverse("admin:ecommerce_coverde_utilizador_change", args=[obj.produtor.id])
        return mark_safe(f'<a href="{url}">{obj.produtor.get_full_name()}</a>')
    produtor_link.short_description = 'Produtor'

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="50" style="object-fit: cover;" />',
                obj.imagem.url
            )
        return "-"
    imagem_preview.short_description = 'Imagem'

    def marcar_como_indisponivel(self, request, queryset):
        updated = queryset.update(disponivel=False)
        self.message_user(request, f"{updated} produtos marcados como indisponíveis")
    marcar_como_indisponivel.short_description = "Marcar selecionados como indisponíveis"

    def marcar_como_biologico(self, request, queryset):
        updated = queryset.update(certificado_biologico=True)
        self.message_user(request, f"{updated} produtos marcados como biológicos")
    marcar_como_biologico.short_description = "Marcar selecionados como biológicos"

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem_menu', 'icone')
    search_fields = ('nome', 'descricao')
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ('ordem_menu', 'icone')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilizador_link', 'data_criacao', 'status', 'total', 'metodo_pagamento')
    search_fields = ('utilizador__email', 'utilizador__first_name', 'utilizador__last_name')
    list_filter = ('status', 'metodo_pagamento', 'data_criacao')
    readonly_fields = ('data_criacao', 'total')
    date_hierarchy = 'data_criacao'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('utilizador')

    def utilizador_link(self, obj):
        url = reverse("admin:ecommerce_coverde_utilizador_change", args=[obj.utilizador.id])
        return mark_safe(f'<a href="{url}">{obj.utilizador.get_full_name()}</a>')
    utilizador_link.short_description = 'Cliente'

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'preco', 'subtotal')
    search_fields = ('produto__nome', 'pedido__utilizador__email')

    def subtotal(self, obj):
        return f"{obj.subtotal:.2f}€"
    subtotal.short_description = 'Subtotal'

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilizador_link', 'atualizado_em', 'total')
    search_fields = ('utilizador__email',)
    readonly_fields = ('atualizado_em',)

    def utilizador_link(self, obj):
        url = reverse("admin:ecommerce_coverde_utilizador_change", args=[obj.utilizador.id])
        return mark_safe(f'<a href="{url}">{obj.utilizador.get_full_name()}</a>')
    utilizador_link.short_description = 'Utilizador'

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('carrinho', 'produto', 'quantidade', 'preco', 'subtotal')
    search_fields = ('produto__nome', 'carrinho__utilizador__email')

    def subtotal(self, obj):
        return f"{obj.subtotal:.2f}€"
    subtotal.short_description = 'Subtotal'

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('utilizador_link', 'produto_link', 'criado_em')
    search_fields = ('utilizador__email', 'produto__nome')
    list_filter = ('criado_em',)

    def utilizador_link(self, obj):
        url = reverse("admin:ecommerce_coverde_utilizador_change", args=[obj.utilizador.id])
        return mark_safe(f'<a href="{url}">{obj.utilizador.get_full_name()}</a>')
    utilizador_link.short_description = 'Utilizador'

    def produto_link(self, obj):
        url = reverse("admin:ecommerce_coverde_produto_change", args=[obj.produto.id])
        return mark_safe(f'<a href="{url}">{obj.produto.nome}</a>')
    produto_link.short_description = 'Produto'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'assunto', 'data_envio')
    search_fields = ('nome', 'email', 'assunto', 'mensagem')
    readonly_fields = ('data_envio',)
    ordering = ('-data_envio',)
    list_filter = ('data_envio',)