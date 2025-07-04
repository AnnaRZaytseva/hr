from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods
from .models import  Vacancy
# from .forms import VacancyForm, EditVacancyForm
import json 
from .ai.ai_func import begin, get_q
from django.contrib.auth import authenticate, login, logout

messages = {}

@csrf_exempt
def vacancyinfo(request):
    vacancies = Vacancy.objects.filter(isActive=True)
    vacancies_data = {vacancy.id:{'id':vacancy.id,
                                 'title':vacancy.title,
                                 'description':vacancy.description,
                                 'requirements':vacancy.requirements,
                                 'responsibilities':vacancy.responsibilities,
                                 'conditions':vacancy.conditions,
                                 'isActive':vacancy.isActive}
                                 for vacancy in vacancies}
    # print(vacancies)
    # print(vacancies_data)
    if request.method == 'POST':
        logout(request)
        return render(request, 'employee/index.html',{'vacancies': vacancies, 'vacancies_json':json.dumps(vacancies_data)})
    return render(request, 'employee/index.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})
   
@csrf_exempt
def get_question(request):
    global messages

    if request.method == 'GET':
        messages = get_q(messages)

        question = messages['all'][-1]
        return JsonResponse({'question': str(question)})

@csrf_exempt
def get_question_first(request):
    global messages
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            messages = begin(data['vacancy_id'])
            return JsonResponse({'question': str(messages['all'][-1])})
        except:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)
        

    
@csrf_exempt
def start_interview(request):
    if request.method == 'POST':
        vacancy_id = request.POST.get('vacancy_id')
        return JsonResponse({'question': f'Первый вопрос по вакансии {vacancy_id}'})
    return JsonResponse({}, status=400)