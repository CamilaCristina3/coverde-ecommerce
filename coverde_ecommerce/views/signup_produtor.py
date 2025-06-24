from pyexpat.errors import messages
from django.shortcuts import redirect, render

from coverde_ecommerce.forms import ProdutorRegistrationForm
from coverde_ecommerce.views import login
from coverde_ecommerce.views.auth import get_dashboard_redirect


def signup_produtor(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_redirect(request.user))

    if request.method == 'POST':
        form = ProdutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta de produtor criada!')
            return redirect('coverde_ecommerce:produtor_dashboard')
    else:
        form = ProdutorRegistrationForm()

    return render(request, 'coverde_ecommerce/auth/signup_produtor.html', {'form': form})
