from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

# Views principais
from loja.views.home import IndexView
from loja.views.auth.login import LoginView
from loja.views.auth.registo import SignupConsumidorView, SignupProdutorView

urlpatterns = [
    # Área administrativa
    path('admin/', admin.site.urls),

    # Página inicial
    path('', IndexView.as_view(), name='index'),

    # Autenticação
    path('auth/', include([
        path('login/', LoginView.as_view(), name='login'),
        path('signup/consumidor/', SignupConsumidorView.as_view(), name='signup_consumidor'),
        path('signup/produtor/', SignupProdutorView.as_view(), name='signup_produtor'),
    ])),

    # Aplicação principal
    path('loja/', include(('loja.urls', 'loja'), namespace='loja')),

    # Dashboard (caso tenha)
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
]

# Servir arquivos estáticos e media em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
