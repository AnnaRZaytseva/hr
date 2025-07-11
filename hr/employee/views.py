from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods
from .models import  Vacancy, InterviewResult
# from .forms import VacancyForm, EditVacancyForm
import json 
import ast
# from .ai.ai_func import begin, get_q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from langchain_core.messages import HumanMessage, SystemMessage
from .GigaChat import giga
from .constants import SYSTEM_PROMPT, ANALYSIS_SYSTEM_PROMPT

# @login_required
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

def begin(vacancy_id):
    """Генерирует список вопросов по вакансии"""
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        
        full_description = (
            f"Наименование вакансии: {vacancy.title}\n\n"
            f"Описание вакансии: {vacancy.description}\n\n"
            f"Требования к кандидату: {vacancy.requirements}\n\n"
            f"Обязанности кандидата: {vacancy.responsibilities}\n\n"
            f"Условия для кандидата: {vacancy.conditions}"
        )
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=full_description)
        ]
        
        response = giga.invoke(messages)
        questions = ast.literal_eval(response.content)
        
        if not isinstance(questions, list):
            raise ValueError("Нейросеть не вернула список вопросов")

        # print("Сгенерировано вопросов "+ str(len(questions)))
        
        return questions
        
    except Vacancy.DoesNotExist:
        raise ValueError("Вакансия не найдена")
    except Exception as e:
        raise ValueError(f"Ошибка генерации вопросов: {str(e)}")


@csrf_exempt
def handle_interview(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        session_data = request.session.get('interview_data', {})
        # Инициализация нового собеседования
        if 'vacancy_id' in data and not session_data:
            vacancy_id = data['vacancy_id']
            try:
                questions = begin(vacancy_id)  # Генерация вопросов
                
                vacancy = Vacancy.objects.get(id=vacancy_id)
                
                request.session['interview_data'] = {
                    'questions': questions,
                    'answers': {},
                    'current_index': 0,
                    'vacancy_id':vacancy.id,
                    'vacancy_title':vacancy.title,
                    'vacancy_description':vacancy.description,
                    'vacancy_requirements':vacancy.requirements,
                    'vacancy_responsibilities':vacancy.responsibilities,
                    'vacancy_conditions':vacancy.conditions
                }
                session_data = request.session['interview_data']

                return JsonResponse({
                    'status': 'in_progress',
                    'question': questions[0],
                    'progress': {
                        'current': 1,
                        'total': len(questions)
                    }
                })

            except Vacancy.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Вакансия не найдена'}, status=404)

        # Проверка активного собеседования
        if not session_data:
            return JsonResponse({'status': 'error', 'message': 'Собеседование не начато'}, status=400)

        # Обработка ответа
        if 'answer' in data:
            current_idx = session_data['current_index']
            session_data['answers'][session_data['questions'][current_idx]] = data['answer']
            session_data['current_index'] += 1
            request.session.modified = True

        # Проверка завершения
        if session_data['current_index'] >= len(session_data['questions']):
            # del request.session['interview_data']  # Очищаем сессию
            return JsonResponse({
                'status': 'completed',
                'result': {
                    'score': len(session_data['answers']),
                    'total': len(session_data['questions'])
                }
            })

        # Возврат следующего вопроса
        next_question = session_data['questions'][session_data['current_index']]
        return JsonResponse({
            'status': 'in_progress',
            'question': next_question,
            'progress': {
                'current': session_data['current_index'] + 1,
                'total': len(session_data['questions'])
            }
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def end_interview(request):
    try:
        # Проверка аутентификации пользователя
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Требуется авторизация'}, status=401)

        # Получаем данные из сессии
        interview_data = request.session.get('interview_data')
        # print(interview_data)
        if not interview_data:
            del request.session['interview_data']
            return JsonResponse({'error': 'Данные собеседования не найдены'}, status=404)
        
        # Формируем структурированные данные собеседования
        interview_info = json.dumps({
            'vacancy': {
                'id': interview_data.get('vacancy_id'),
                'title':interview_data.get('title'),
                'description':interview_data.get('description'),
                'requirements':interview_data.get('requirements'),
                'responsibilities':interview_data.get('responsibilities'),
                'conditions':interview_data.get('conditions'),
                'isActive':interview_data.get('isActive')

            },
            'qa_pairs': [
                {
                    'question': q,
                    'answer': interview_data['answers'].get(q, 'Нет ответа')
                }
                for q in interview_data['questions']
            ]
        })
        
        # Отправляем на анализ нейросети
        messages = [
            SystemMessage(content=ANALYSIS_SYSTEM_PROMPT),
            HumanMessage(content=interview_info)
        ]
        
        analysis_result = ast.literal_eval(giga.invoke(messages).content)
        
        # Получаем или создаем объект вакансии
        try:
            vacancy = Vacancy.objects.get(id=interview_data['vacancy_id'])
        except Vacancy.DoesNotExist:
            return JsonResponse({'error': 'Вакансия не найдена'}, status=404)
        
        # Создаем запись в базе данных
        interview_result = InterviewResult.objects.create(
            user=request.user,
            vacancy=vacancy,
            qa_pairs=[
                {
                    'question': q,
                    'answer': interview_data['answers'].get(q, 'Нет ответа')
                }
                for q in interview_data['questions']
            ],
            score_percentage=analysis_result[0].rstrip('%'),  # Удаляем символ % если он есть
            assessment_text=analysis_result[1]
        )
        
        # Очищаем сессию
        del request.session['interview_data']
        
        return JsonResponse({
            'status': 'success',
            'score_percentage': interview_result.score_percentage,
            'interview_id': interview_result.id  # Возвращаем ID созданной записи
        })
        
    except Exception as e:
        if 'interview_data' in request.session:
            del request.session['interview_data']
        return JsonResponse({'error': str(e)}, status=500)