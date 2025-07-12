from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import Avg, Count

from employee.models import Vacancy, InterviewResult
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json 
# Create your views here.

@login_required
@csrf_exempt
def hr_profile(request):
    vacancies = Vacancy.objects.annotate(
        interviews=Count('interview_results')
    ).only(
        'id',
        'title',
        'description',
        'requirements', 
        'responsibilities',
        'conditions',
        'isActive'
    )
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
        
    general_stat = {'avg_score_percentage':round(InterviewResult.objects.aggregate(avg_score_percentage=Avg('score_percentage'))['avg_score_percentage'], 2),
                              'completed_count':InterviewResult.objects.aggregate(count=Count(1))['count'],
                              'active_vacancies_count':Vacancy.objects.filter(isActive = True).aggregate(count=Count(1))['count']}

    return render(request, 'employer/hr_ui.html',{'vacancies': vacancies,
                                                 'vacancies_json':json.dumps(vacancies_data),
                                                 'general_stat':general_stat})

    # return render(request, 'employer/hr_ui.html',{'vacancies': vacancies,
    #                                              'vacancies_json':json.dumps(vacancies_data)})
    
    
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
    
    
@csrf_exempt
@login_required
def get_vacancy_report(request):
    if request.method == 'POST':
        # print(request.POST)
        # print("\n\n", request.body)
        try:
            data = json.loads(request.body)
            vacancy_id=data.get('vacancy_id')
            # report_info = InterviewResult.objects.filter(vacancy = vacancy_id)
            
            
            report_info = InterviewResult.objects.filter(vacancy_id=vacancy_id).select_related('vacancy')

            formatted_data = []
            for result in report_info:  # Итерируемся по каждому объекту
                qa_list = []
                for qa in result.qa_pairs:  # Перебираем все Q&A
                    qa_list.append({
                        'question': qa.get('question', ''),
                        'answer': qa.get('answer', '')
                    })
                
                formatted_data.append({
                    'id': result.id,
                    'fullname': result.user.get_full_name(),
                    'email': result.user.email,
                    'vacancy_title': result.vacancy.title if result.vacancy else '',  # Доступ к vacancy
                    'per': f"{result.score_percentage}%",
                    'ai_result':result.assessment_text,
                    'qa_pairs': qa_list  # Все вопросы и ответы
                })
                
                print(formatted_data)
                return JsonResponse({'report_info': formatted_data}, safe=False)
            
            
            return JsonResponse({'status': 'success', 'id': vacancy_id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)


