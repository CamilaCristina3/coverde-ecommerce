from django.shortcuts import render, redirect
from loja.models import MensagemDeContacto

def contactos_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        MensagemDeContacto.objects.create(
            nome=nome,
            email=email,
            mensagem=mensagem
        )

        return render(request, 'loja/contacto_sucesso.html')

    return render(request, 'loja/contacto.html')
