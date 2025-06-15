from django.shortcuts import render

def index_view(request):
    return render(request, 'ecommerce_coverde/core/index.html')