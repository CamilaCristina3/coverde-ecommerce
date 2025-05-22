# dashboard/views.py
from django.shortcuts import render
from django.http import HttpResponse

def dashboard_home(request):
    return HttpResponse("Dashboard em construção.")
