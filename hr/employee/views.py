from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import  Vacancy
from .forms import VacancyForm
import json 
from .ai.ai_func import begin, get_q

messages = {}


# def vacancyinfo(request):
#    username = request.user.username
#    return render(request, 'employee/index.html', {'username': username})
@csrf_exempt
def new_vacancy(request):
   if request.method == 'POST':
      form = VacancyForm(request.POST)
      if form.is_valid():
         form.save()
   form  = VacancyForm()
   data = {'form':form}
   return render(request, 'employee/form.html', data)

def vacancy_list(request):
   vacancies = Vacancy.objects.all()
   vacancies_data = {vacancy.id:{'title':vacancy.title,
                                 'description':vacancy.description,
                                 'requirements':vacancy.requirements,
                                 'responsibilities':vacancy.responsibilities,
                                 'conditions':vacancy.conditions}
                                 for vacancy in vacancies}
   
   return render(request, 'employee/index.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})
   
   
@csrf_exempt
def vacancyinfo(request):
   username = request.user.username
   return render(request, 'employee/index.html', {'username': username})
   if request.method == 'POST':
      try:
         data = json.loads(request.body.decode('utf-8'))
         answer = data.get('answer')

         messages['all'].append(answer)

      except json.JSONDecodeError:
         return JsonResponse({'error': 'Invalid JSON format'}, status=400)
      except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)
   return render(request, 'employee/index.html')
   
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

    if request.method == 'GET':
        messages = begin()
        question = messages['all'][-1]

        if 'конец' in str(question).lower():
            question = 'КОНЕЦ'
        return JsonResponse({'question': str(question)})