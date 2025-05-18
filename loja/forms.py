from django import forms
from django.contrib.auth.forms import UserCreationForm
from loja.models import Utilizador

class ConsumidorForm(UserCreationForm):
    class Meta:
        model = Utilizador
        fields = ['email', 'password1', 'password2']
        labels = {
            'username': 'Nome de utilizador',
            'email': 'Email',
            'password1': 'Palavra-passe',
            'password2': 'Confirmar palavra-passe',
        }

class ProdutorForm(UserCreationForm):
    class Meta:
        model = Utilizador
        fields = [ 'email', 'nif', 'morada', 'password1', 'password2']
        labels = {
            'username': 'Nome de utilizador',
            'email': 'Email',
            'nif': 'NIF',
            'morada': 'Morada de faturação',
            'password1': 'Palavra-passe',
            'password2': 'Confirmar palavra-passe',
        }
