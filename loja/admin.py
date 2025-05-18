from django.contrib import admin
from .models import Utilizador, Categoria, Produto, Encomenda

admin.site.register(Utilizador)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Encomenda)