from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Vacancy
import json

# def vacancy_list(request):
#    vacancies = {}
#    for vacancy in Vacancy.objects.all():
#       vacancies[vacancy.id] = {
#          'title': vacancy.title,
#          'description': vacancy.description
#       }
   
#    return JsonResponse(vacancies)

def vacancy_list(request):
   vacancies = Vacancy.objects.all()
   vacancies_data = {vacancy.id:{'title':vacancy.title,
                                 'description':vacancy.description}
                                 for vacancy in vacancies}
   
   return render(request, 'employee/index.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})

def vacancyinfo(request):
   return render(request, 'employee/index.html')
