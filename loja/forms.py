from django import forms
from loja.models import Produto
from django.contrib.auth.forms import UserCreationForm
from loja.models import Utilizador

class ConsumidorSignupForm(UserCreationForm):
    class Meta:
        model = Utilizador
        fields = [
            'first_name', 'last_name', 'email',
            'telefone', 'nif', 'morada',
            'codigo_postal', 'localidade'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = Utilizador.TipoUtilizador.CONSUMIDOR
        if commit:
            user.save()
        return user

class ProdutorSignupForm(UserCreationForm):
    class Meta:
        model = Utilizador
        fields = [
            'first_name', 'last_name', 'email',
            'telefone', 'nif', 'morada',
            'codigo_postal', 'localidade'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = Utilizador.TipoUtilizador.PRODUTOR
        if commit:
            user.save()
        return user
    
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['slug', 'produtor']  # Slug é gerado automaticamente, produtor vem da view

        widgets = {
            'data_colheita': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'