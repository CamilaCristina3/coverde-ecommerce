# loja/views/auth/logout.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """Vista para terminar sessão (logout)"""
    logout(request)
    return redirect('index')
