from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from coverde_ecommerce.forms import ConsumidorRegistrationForm
from django.contrib.auth.backends import ModelBackend

def signup_consumidor(request):
    if request.user.is_authenticated:
        return redirect('coverde_ecommerce:produto_list')

    if request.method == 'POST':
        form = ConsumidorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo = 'C'  # Consumidor
            user.save()
            
            # Corrigindo o erro de múltiplos backends
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, 'Conta de consumidor criada com sucesso!')
            return redirect('coverde_ecommerce:produto_list')
    else:
        form = ConsumidorRegistrationForm()

    return render(request, 'coverde_ecommerce/auth/signup_consumidor.html', {'form': form})
