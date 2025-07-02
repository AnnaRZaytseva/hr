from django.urls import path
from . import views

urlpatterns = [
    path('vacancyinfo/', views.vacancy_list, name = 'vacancy_list'),
    path('vacancyinfo/getq/', views.get_question, name='get_question'),
    path('vacancyinfo/getq_first/', views.get_question_first, name='get_question_first'),
    # path('new_vacancy/', views.new_vacancy, name = 'new_vacancy'),
    path('hr_profile/', views.hr_profile, name = 'hr_profile'),
    path('hr_profile/update-vacancy-status/', views.update_vacancy_status, name='update_vacancy_status'),
    path('hr_profile/delete-vacancy/', views.delete_vacancy, name='delete_vacancy-vacancy'),
    path('hr_profile/update-vacancy/', views.update_vacancy, name='update_vacancy'),
]
