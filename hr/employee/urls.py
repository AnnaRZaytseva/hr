from django.urls import path
from . import views

urlpatterns = [
    path('vacancyinfo/', views.vacancy_list, name = 'vacancy_list'),
    path('getq/', views.get_question, name='get_question'),
    path('getq_first/', views.get_question_first, name='get_question_first')
]
