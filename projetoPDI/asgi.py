"""
ASGI config for projetoPDI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

# Carrega variáveis do .env no ambiente (importante fora de Docker)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetoPDI.settings')

application = get_asgi_application()
