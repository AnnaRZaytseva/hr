from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import  Vacancy
from .forms import VacancyForm, EditVacancyForm
import json 
from .ai.ai_func import begin, get_q

messages = {}


# def vacancyinfo(request):
#    username = request.user.username
#    return render(request, 'employee/index.html', {'username': username})
# @csrf_exempt
# def new_vacancy(request):
#     if request.method == 'POST':
#       form = VacancyForm(request.POST)
#       if form.is_valid():
#          form.save()
#     form  = VacancyForm()
#     data = {'form':form}
#     return render(request, 'employee/form.html', data)
@csrf_exempt
def vacancy_list(request):
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
    return render(request, 'employee/index.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})
   
   
# @csrf_exempt
# def vacancyinfo(request):
#     # # Получаем полное имя (если пользователь авторизован)
#     # if request.user.is_authenticated:
#     #     full_name = f"{request.user.first_name} {request.user.last_name}".strip()
#     #     if not full_name:  # Если имя и фамилия не указаны
#     #         full_name = request.user.username  # Используем логин как fallback
#     #         print(full_name)
#     # else:
#     #     full_name = None

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             answer = data.get('answer')
#             messages['all'].append(answer)
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return render(request, 'employee/index.html')
   
@csrf_exempt
def get_question(request):
    global messages

    if request.method == 'GET':
        messages = get_q(messages)

        question = messages['all'][-1]
        return JsonResponse({'question': str(question)})

# @csrf_exempt
# def get_question_first(request):
#     global messages
    
#     if request.method == 'GET':
#         messages = begin()
#         question = messages['all'][-1]

#         if 'конец' in str(question).lower():
#             question = 'КОНЕЦ'
#         return JsonResponse({'question': str(question)})

# @csrf_exempt
# def get_question_first(request):
#     global messages
    
#     if request.method == 'POST':
#         try:
#             # Получаем ID вакансии из тела запроса
#             data = json.loads(request.body)
#             vacancy_id = data.get('vacancy_id')
            
#             if not vacancy_id:
#                 return JsonResponse({'error': 'Vacancy ID not provided'}, status=400)
            
#             # Передаем ID в функцию begin()
#             messages = begin(vacancy_id)
#             question = messages['all'][-1]

#             if 'конец' in str(question).lower():
#                 question = 'КОНЕЦ'
            
#             return JsonResponse({'question': str(question)})
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

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
    
@login_required
@csrf_exempt
def hr_profile(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_profile')
    else:
        form  = VacancyForm()
            
    vacancies = Vacancy.objects.only('id',
                                    'title',
                                    'description',
                                    'requirements', 
                                    'responsibilities',
                                    'conditions',
                                    'interviews',
                                    'isActive')
    vacancies_data = [{
                        'id': vacancy.id,
                        'title': vacancy.title,
                        'description': vacancy.description,
                        'requirements': vacancy.requirements,
                        'responsibilities': vacancy.responsibilities,
                        'conditions': vacancy.conditions,
                        'interviews': vacancy.interviews,
                        'isActive': vacancy.isActive} 
                      for vacancy in vacancies]

    return render(request, 'employee/hr_ui.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data),
                                                 'form':form})
    
@csrf_exempt
def update_vacancy(request):
    try:
        data = json.loads(request.body)
        # print(data)
        Vacancy.objects.filter(id=data['vacancy_id']).update(title=data['title'],
                                                            description=data['description'],
                                                            requirements=data['requirements'],
                                                            responsibilities=data['responsibilities'],
                                                            conditions=data['conditions'])
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    
@csrf_exempt
def update_vacancy_status(request):
    try:
        data = json.loads(request.body)
        # id = request.POST.get('vacancy_id')
        print(data)
        Vacancy.objects.filter(id=data['vacancy_id']).update(isActive=data['is_active'])
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
# @require_http_methods(["DELETE"])
@csrf_exempt
def delete_vacancy(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        # print(data)
        vacancy = Vacancy.objects.get(id=data['vacancy_id'])
        vacancy.delete()
        return JsonResponse({'status': 'success'}, status=204)
    except Vacancy.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
@csrf_exempt
def start_interview(request):
    if request.method == 'POST':
        vacancy_id = request.POST.get('vacancy_id')
        return JsonResponse({'question': f'Первый вопрос по вакансии {vacancy_id}'})
    return JsonResponse({}, status=400)