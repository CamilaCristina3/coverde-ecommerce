from pyexpat.errors import messages
from django.contrib.auth import login, get_backends
from django.shortcuts import redirect, render

from coverde_ecommerce.forms import ProdutorRegistrationForm

def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect('coverde_ecommerce:dashboard_produtor')

    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo = 'P'
            user.save()

            # Informar explicitamente o backend
            user.backend = get_backends()[0].__module__ + '.' + get_backends()[0].__class__.__name__
            login(request, user)

            messages.success(request, 'Conta de produtor criada com sucesso!')
            return redirect('coverde_ecommerce:dashboard_produtor')
    else:
        form = ProdutorRegistrationForm()

    return render(request, 'coverde_ecommerce/auth/signup_produtor.html', {'form': form})
