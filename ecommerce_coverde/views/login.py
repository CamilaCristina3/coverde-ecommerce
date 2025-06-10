from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView

class Login(View):
    def get(self, request):
       return render(request, 'ecommerce_coverde/auth/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Autenticação baseada no e-mail (deve funcionar se AUTH_USER_MODEL estiver corretamente definido)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "E-mail ou senha inválidos. Tente novamente.")
            return render(request, "auth/login.html")


   