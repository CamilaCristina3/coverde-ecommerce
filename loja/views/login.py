from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from loja.models import Utilizador

class LoginView(DjangoLoginView):
    template_name = 'pt/auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.tipo == Utilizador.TipoUtilizador.PRODUTOR:
            return reverse_lazy('loja:dashboard')
        else:
            return reverse_lazy('loja:produtos')
