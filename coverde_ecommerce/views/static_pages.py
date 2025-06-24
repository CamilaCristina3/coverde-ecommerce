from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

def contacto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        
        send_mail(
            f'Mensagem de {nome}',
            mensagem,
            email,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.success(request, 'A sua mensagem foi enviada com sucesso!')
        return redirect('contacto')
    
    return render(request, 'static/contacto.html')