from django.urls import path
from . import views

urlpatterns = [
    path('hr_profile/', views.hr_profile, name = 'hr_profile'),
    path('hr_profile/add-vacancy/', views.add_vacancy, name='add_vacancy'),
    path('hr_profile/update-vacancy-status/', views.update_vacancy_status, name='update_vacancy_status'),
    path('hr_profile/delete-vacancy/', views.delete_vacancy, name='delete_vacancy-vacancy'),
    path('hr_profile/update-vacancy/', views.update_vacancy, name='update_vacancy'),
    path('hr_profile/get-vacancy-report/', views.get_vacancy_report, name='get_vacancy_report'),
]