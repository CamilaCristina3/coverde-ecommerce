from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import Utilizador, Produto
from .models import Pedido

# ========== FORMULÁRIOS DE AUTENTICAÇÃO ==========
class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email *",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'exemplo@email.com'
        }),
        help_text="Será usado para fazer login no sistema"
    )
    
    first_name = forms.CharField(
        label="Primeiro Nome *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Seu primeiro nome'
        })
    )
    
    last_name = forms.CharField(
        label="Último Nome",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Seu último nome'
        })
    )
    
    telefone = forms.CharField(
        label="Telefone",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '+351 912 345 678'
        })
    )
    
    password1 = forms.CharField(
        label="Criar Senha *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '••••••••',
            'data-toggle': 'password'
        }),
        help_text="Mínimo 8 caracteres com pelo menos 1 letra maiúscula e 1 número"
    )
    
    password2 = forms.CharField(
        label="Confirmar Senha *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '••••••••'
        })
    )
    
    termos_condicoes = forms.BooleanField(
        label="Li e aceito os Termos e Condições *",
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = Utilizador
        fields = ['first_name', 'last_name', 'email', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields:
            if field not in ['termos_condicoes']:
                self.fields[field].widget.attrs['class'] += ' mb-3'

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'exemplo@email.com'
        })
    )
    
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '••••••••',
            'data-toggle': 'password'
        })
    )

    remember_me = forms.BooleanField(
        label="Lembrar-me",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields:
            self.fields[field].widget.attrs['class'] += ' mb-3'

# ========== FORMULÁRIOS DE REGISTRO ==========
class ProdutorRegistrationForm(BaseRegistrationForm):
    nif = forms.CharField(
        label="NIF *",
        max_length=9,
        validators=[RegexValidator(r'^\d{9}$', 'NIF deve conter exatamente 9 dígitos')],
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '123456789'
        })
    )
    
    nome_empresa = forms.CharField(
        label="Nome da Empresa *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Minha Empresa Lda'
        })
    )
    
    morada = forms.CharField(
        label="Morada *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Rua, Número, Andar'
        })
    )
    
    codigo_postal = forms.CharField(
        label="Código Postal *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '1234-567'
        })
    )
    
    localidade = forms.CharField(
        label="Localidade *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Lisboa'
        })
    )

    class Meta(BaseRegistrationForm.Meta):
        fields = BaseRegistrationForm.Meta.fields + [
            'nif', 'nome_empresa', 'morada', 
            'codigo_postal', 'localidade'
        ]

class ConsumidorRegistrationForm(BaseRegistrationForm):
    morada = forms.CharField(
        label="Morada *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Rua, Número, Andar'
        })
    )
    
    codigo_postal = forms.CharField(
        label="Código Postal *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '1234-567'
        })
    )
    
    localidade = forms.CharField(
        label="Localidade *",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Lisboa'
        })
    )

    class Meta(BaseRegistrationForm.Meta):
        fields = BaseRegistrationForm.Meta.fields + [
            'morada', 'codigo_postal', 'localidade'
        ]

# ========== FORMULÁRIOS DE PERFIL/PRODUTO ==========
class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = ['first_name', 'last_name', 'email', 'telefone', 'nif', 'imagem_perfil']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'slug', 'descricao', 'preco', 'unidade', 'stock',
            'imagem', 'data_colheita', 'certificado_biologico',
            'categoria', 'destaque', 'disponivel'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nome do produto'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-gerado',
                'readonly': True
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição detalhada do produto'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'unidade': forms.Select(attrs={
                'class': 'form-select'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'data_colheita': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'certificado_biologico': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'destaque': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
            'disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
        }
        labels = {
            'nome': 'Nome do Produto',
            'slug': 'URL Amigável',
            'descricao': 'Descrição',
            'preco': 'Preço (€)',
            'unidade': 'Unidade de Medida',
            'stock': 'Quantidade em Stock',
            'imagem': 'Imagem do Produto',
            'data_colheita': 'Data de Colheita/Produção',
            'certificado_biologico': 'Produto Biológico',
            'categoria': 'Categoria',
            'destaque': 'Destacar este produto',
            'disponivel': 'Disponível para venda'
        }
        help_texts = {
            'slug': 'Identificador único para URLs (gerado automaticamente)',
            'data_colheita': 'Data estimada de colheita ou produção',
            'certificado_biologico': 'Marque se o produto tem certificação biológica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True
        else:
            self.fields['slug'].required = False

class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'endereco_entrega', 'metodo_pagamento']
        widgets = {
            'endereco_entrega': forms.Textarea(attrs={'rows': 3}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['endereco_entrega', 'metodo_pagamento']
        widgets = {
            'endereco_entrega': forms.Textarea(attrs={'rows': 3}),
            'metodo_pagamento': forms.RadioSelect(choices=[
                ('cartao', 'Cartão de Crédito'),
                ('transferencia', 'Transferência Bancária'),
                ('mbway', 'MBWay'),
            ])
        }