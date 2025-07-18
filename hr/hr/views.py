from django.shortcuts import render
from employee.models import Vacancy
import json
from django.contrib.auth import logout

def index(request):
    is_hr = request.user.groups.filter(name='hr').exists()
    context = {
        'is_hr': is_hr
    }
    if request.method == 'POST':
        logout(request)
        return render(request, 'main/main.html', context)
    return render(request, 'main/main.html', context)
