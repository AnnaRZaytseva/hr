from django.db import models
from django.forms.widgets import TextInput

class Vacancy(models.Model):
    title = models.CharField('Название',max_length=50)
    description = models.TextField('Описание')
    requirements = models.TextField('Требования')
    responsibilities = models.TextField('Обязанности')
    conditions = models.TextField('Условия')
    interviews = models.IntegerField('Пройдено собеседований',default=0)
    isActive = models.BooleanField('Отображается',default=False)
    
    def _str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-id']
        