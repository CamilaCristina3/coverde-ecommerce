from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import Utilizador, Produto, Pedido
from django.utils import timezone

# ========== FORMULÁRIOS DE AUTENTICAÇÃO ==========
class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email *",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'exemplo@email.com',
            'aria-describedby': 'emailHelp'
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
            'placeholder': '+351 912 345 678',
            'pattern': '^(\+351)?[ ]?[9][1236][ ]?[0-9]{3}[ ]?[0-9]{3}$'
        }),
        help_text="Formato: +351 912 345 678"
    )
    
    password1 = forms.CharField(
        label="Criar Senha *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '••••••••',
            'data-toggle': 'password',
            'aria-describedby': 'passwordHelp'
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
            'class': 'form-check-input',
            'aria-required': 'true'
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
        label="Email *",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'exemplo@email.com',
            'autocomplete': 'username'
        })
    )

    password = forms.CharField(
        label="Senha *",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '••••••••',
            'data-toggle': 'password',
            'autocomplete': 'current-password'
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
            'placeholder': '123456789',
            'inputmode': 'numeric'
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
        validators=[RegexValidator(r'^\d{4}-\d{3}$', 'Código Postal deve estar no formato 1234-567')],
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
        validators=[RegexValidator(r'^\d{4}-\d{3}$', 'Código Postal deve estar no formato 1234-567')],
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
        widgets = {
            'imagem_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'aria-label': 'Selecione uma imagem de perfil'
            })
        }

class ProdutoForm(forms.ModelForm):
    data_colheita = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        }),
        label="Data de Colheita/Produção"
    )
    
    certificado_biologico = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': 'width: 20px; height: 20px;'
        }),
        label="Produto Biológico"
    )

    class Meta:
        model = Produto
        fields = [
            'nome', 'slug', 'descricao', 'preco', 'unidade', 'stock',
            'imagem', 'categoria', 'destaque', 'disponivel'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['slug'].widget.attrs['readonly'] = True
        else:
            self.fields['slug'].required = False

class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        label="E-mail *",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
            'autocomplete': 'email'
        })
    )

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'endereco_entrega', 'metodo_pagamento']
        widgets = {
            'endereco_entrega': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Rua, Número, Código Postal, Localidade'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pagamento': forms.Select(attrs={'class': 'form-select'})
        }

class CheckoutForm(forms.ModelForm):
    metodo_pagamento = forms.ChoiceField(
        choices=[
            ('cartao', 'Cartão de Crédito'),
            ('transferencia', 'Transferência Bancária'),
            ('mbway', 'MBWay'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="Método de Pagamento *"
    )
    
    class Meta:
        model = Pedido
        fields = ['endereco_entrega', 'metodo_pagamento']
        widgets = {
            'endereco_entrega': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Rua, Número, Código Postal, Localidade'
            }),
        }