import email

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from httpx import request
from .forms import UserRegistrationForm
from django.contrib.auth.models import User


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
        password = request.POST.get('password')

        print(f"Attempting login with email: {email}, username: {username}, password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверный логин или пароль")
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')
    
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'registration/login.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data
            email = user_form.cleaned_data['email']
            if User.objects.filter(email=email).exists()==False:
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})




