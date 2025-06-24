"""
WSGI config for projetoPDI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Define o caminho base do projeto (nível do manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetoPDI.settings')

# Cria a aplicação WSGI
application = get_wsgi_application()
