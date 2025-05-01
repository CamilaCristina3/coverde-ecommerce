from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from loja.models import User, Categoria, Produto, ImagemProduto, MensagemDeContacto

# === Personalização do UserAdmin ===
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'primeiro_nome', 'ultimo_nome', 'perfil', 'is_staff')
    list_filter = ('perfil', 'is_staff', 'is_superuser')
    search_fields = ('email', 'primeiro_nome', 'ultimo_nome')
    ordering = ('email',)
    filter_horizontal = ('categorias_produzidas',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {
            'fields': (
                'primeiro_nome', 'ultimo_nome', 'telemovel', 'perfil',
                'foto_perfil', 'descricao', 'localidade'
            )
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Categorias produzidas', {'fields': ('categorias_produzidas',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'primeiro_nome', 'ultimo_nome', 'telemovel',
                'perfil', 'password1', 'password2'
            ),
        }),
    )

# === Imagens Inline no Produto ===
class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

# === Produto ===
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'produtor', 'preco', 'modo_producao')
    list_filter = ('categoria', 'modo_producao')
    search_fields = ('nome', 'descricao')
    inlines = [ImagemProdutoInline]

# === Categoria ===
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# === Mensagens de Contacto ===
class MensagemDeContactoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_envio')
    search_fields = ('nome', 'email', 'mensagem')
    readonly_fields = ('nome', 'email', 'mensagem', 'data_envio')

# === Registro dos modelos com admin personalizados ===
admin.site.register(User, UserAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(ImagemProduto)  # Inline já está no Produto, mas pode ser acessado diretamente também
admin.site.register(MensagemDeContacto, MensagemDeContactoAdmin)
