from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views import View
from employee.models import Vacancy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json 
# Create your views here.

@csrf_exempt
@login_required
def hr_profile(request):
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

    return render(request, 'employer/hr_ui.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data)})
    
    
@csrf_exempt
@login_required
def add_vacancy(request):
    if request.method == 'POST':
        # print(request.POST)
        # print("\n\n", request.body)
        try:
            data = json.loads(request.body)
            
            new_vacancy = Vacancy(
                title=data.get('title'),
                description=data.get('description'),
                requirements=data.get('requirements'),
                responsibilities=data.get('responsibilities'),
                conditions=data.get('conditions')
            )
            new_vacancy.save()
            # print(request.POST)
            # return redirect(reverse('hr_profile'))
            return JsonResponse({'status': 'success', 'id': new_vacancy.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

@csrf_exempt
@login_required
def update_vacancy(request):
    if request.method == 'POST':
        # print(request.POST)
        # print("\n\n", request.body)
        try:
            data = json.loads(request.body)
            vacancy_id=data.get('vacancy_id')
            Vacancy.objects.filter(id = vacancy_id).update(
                title=data.get('title'),
                description=data.get('description'),
                requirements=data.get('requirements'),
                responsibilities=data.get('responsibilities'),
                conditions=data.get('conditions')
            )
            return JsonResponse({'status': 'success', 'id': vacancy_id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

# @csrf_exempt
# @login_required
# def update_vacancy(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             Vacancy.objects.filter(id=data['vacancy_id']).update(
#                 title=data.get('title'),
#                 description=data.get('description'),
#                 requirements=data.get('requirements'),
#                 responsibilities=data.get('responsibilities'),
#                 conditions=data.get('conditions')
#             )
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
    
    
@csrf_exempt
@login_required
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
@login_required
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