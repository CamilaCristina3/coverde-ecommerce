# loja/views/auth/__init__.py

from .login import LoginView
from .logout import logout_view
from .registo import SignupConsumidorView, SignupProdutorView
from .verificacao_email import SignupEmailVerificationView

__all__ = [
    'LoginView',
    'logout_view',
    'SignupConsumidorView',
    'SignupProdutorView',
    'SignupEmailVerificationView',
]
