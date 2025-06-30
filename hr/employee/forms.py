from .models import Vacancy
from django.forms import ModelForm, TextInput, Textarea

class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title',
                  'description',
                  'requirements',
                  'responsibilities',
                  'conditions']
        
        widgets = {
            "title":TextInput(attrs={
                'class':'classname',
                'placeholder':'Название вакансии'
            }),
            "description":Textarea(attrs={
                'class':'classname',
                'placeholder':'Описание'
            }),
            "requirements":Textarea(attrs={
                'class':'classname',
                'placeholder':'Требования'
            }),
            "responsibilities":Textarea(attrs={
                'class':'classname',
                'placeholder':'Обязанности'
            }),
            "conditions":Textarea(attrs={
                'class':'classname',
                'placeholder':'Условия'
            })
        }