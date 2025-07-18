from django.urls import path
from . import views

urlpatterns = [
    path('vacancyinfo/', views.vacancyinfo, name = 'vacancyinfo'),
    # path('vacancyinfo/getq/', views.get_question, name='get_question'),
    # path('vacancyinfo/getq_first/', views.get_question_first, name='get_question_first'),
    path('vacancyinfo/handle_interview/', views.handle_interview, name='handle_interview'),
    path('vacancyinfo/end_interview/', views.end_interview, name='end_interview'),
]
