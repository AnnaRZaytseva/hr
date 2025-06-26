from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def login(request):
    return render(request, 'accounts/login.html')
