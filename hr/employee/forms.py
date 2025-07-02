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
                'id':"title1",
                'name':"title",
                'placeholder':"Например: Frontend-разработчик"
            }),
            "description":Textarea(attrs={
                'id':"description1",
                'name':"description"
            }),
            "requirements":Textarea(attrs={
                'id':"requirements1",
                'name':"requirements"
            }),
            "responsibilities":Textarea(attrs={
                'id':"responsibilities1",
                'name':"responsibilities"
            }),
            "conditions":Textarea(attrs={
                'id':"conditions1",
                'name':"conditions"
            })
        }
        
class EditVacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['id',
                  'title',
                  'description',
                  'requirements',
                  'responsibilities',
                  'conditions']
        
        widgets = {
            "title":TextInput(attrs={
                'id':"title",
                'name':"title",
                'placeholder':"Например: Frontend-разработчик"
            }),
            "description":Textarea(attrs={
                'id':"description",
                'name':"description"
            }),
            "requirements":Textarea(attrs={
                'id':"requirements",
                'name':"requirements"
            }),
            "responsibilities":Textarea(attrs={
                'id':"responsibilities",
                'name':"responsibilities"
            }),
            "conditions":Textarea(attrs={
                'id':"conditions",
                'name':"conditions"
            })
        }