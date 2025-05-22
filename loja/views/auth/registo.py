from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from loja.forms import ConsumidorSignupForm, ProdutorSignupForm
from loja.models import Utilizador


class SignupConsumidorView(CreateView):
    model = Utilizador
    form_class = ConsumidorSignupForm
    template_name = 'pt/auth/signup_consumidor.html'
    success_url = reverse_lazy('loja:index')

    def form_valid(self, form):
        form.instance.tipo = Utilizador.TipoUtilizador.CONSUMIDOR
        return super().form_valid(form)


class SignupProdutorView(CreateView):
    model = Utilizador
    form_class = ProdutorSignupForm
    template_name = 'pt/auth/signup_produtor.html'
    success_url = reverse_lazy('loja:dashboard')

    def form_valid(self, form):
        form.instance.tipo = Utilizador.TipoUtilizador.PRODUTOR
        return super().form_valid(form)
