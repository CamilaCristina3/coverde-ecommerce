# loja/forms/auth.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemplo@coverde.pt',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label=_("Palavra-passe"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'autocomplete': 'current-password'
        })
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(_("Esta conta está desativada."), code='inactive')
