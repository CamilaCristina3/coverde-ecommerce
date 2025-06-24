from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        if nome and email and mensagem:
            ContactMessage.objects.create(
                nome=nome,
                email=email,
                assunto='Mensagem via formulário de contacto',
                mensagem=mensagem
            )
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contacto em breve.')
            return redirect('contact')  # Certifique-se de que o nome da URL é 'contact'
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'contact.html')
