from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import  Vacancy
import json 

def vacancyinfo(request):
   username = request.user.username
   return render(request, 'employee/index.html', {'username': username})

def vacancy_list(request):
   vacancies = Vacancy.objects.all()
   vacancies_data = {vacancy.id:{'title':vacancy.title,
                                 'description':vacancy.description}
                                 for vacancy in vacancies}
   
   return render(request, 'employee/index.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})