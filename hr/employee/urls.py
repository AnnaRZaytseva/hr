from django.urls import path
from . import views

urlpatterns = [
    # path('vacancyinfo/', views.vacancyinfo, name = 'vacancyinfo')  ,
    path('vacancyinfo/', views.vacancy_list, name = 'vacancy_list') # idk
]