from pyexpat.errors import messages
from django.shortcuts import redirect, render

from backend.ecommerce_coverde.forms import ProdutorRegistrationForm
from backend.ecommerce_coverde.views import login
from backend.ecommerce_coverde.views.auth import get_dashboard_redirect


def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))

    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de produtor criada!')
            return redirect('ecommerce_coverde:produtor_dashboard')
    else:
        form = ProdutorRegistrationForm()

    return render(request, 'ecommerce_coverde/auth/signup_produtor.html', {'form': form})
