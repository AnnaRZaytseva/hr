from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def vacancyinfo(request):
   return HttpResponse("Перечень доступных вакансий и их описаний")
