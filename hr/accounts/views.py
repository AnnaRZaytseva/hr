from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        logout(request)



