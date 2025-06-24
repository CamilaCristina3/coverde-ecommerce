from django.apps import AppConfig

class EcommerceCoverdeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coverde_ecommerce'  # ← CORRETO!
    verbose_name = 'Coverde Ecommerce'
