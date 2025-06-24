from django.urls import path
from . import views

urlpatterns = [
    path('vacancyinfo/', views.vacancyinfo)
]