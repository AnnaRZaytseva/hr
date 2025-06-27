from django.urls import path
from . import views

urlpatterns = [
    path('vacancyinfo/', views.vacancy_list, name = 'vacancy_list')   
]
