from django.shortcuts import render

def quem_somos(request):
    return render(request, 'loja/quem_somos.html')


def como_funciona(request):
    return render(request, 'loja/como_funciona.html')  # ✅ exatamente assim

def novidades(request):
    return render(request, 'loja/novidades.html')

def fala_connosco(request):
    return render(request, 'loja/fala_connosco.html')

def politica_privacidade(request):
    return render(request, 'loja/politica_privacidade.html')