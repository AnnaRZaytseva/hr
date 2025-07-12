from django.db import models
from django.forms.widgets import TextInput
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()

class Vacancy(models.Model):
    title = models.CharField(
        'Название',
        max_length=50
    )
    
    description = models.TextField(
        'Описание'
    )
    
    requirements = models.TextField(
        'Требования'
    )
    
    responsibilities = models.TextField(
        'Обязанности'
    )
    
    conditions = models.TextField(
        'Условия'
    )
    
    isActive = models.BooleanField(
        'Отображается',
        default=False
    )
    
    published_at = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-id']
        
        


User = get_user_model()

class InterviewResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='interview_results'
    )
    
    vacancy = models.ForeignKey(
        'Vacancy',  # Укажите ваше приложение если модель Vacancy в другом месте
        on_delete=models.CASCADE,
        verbose_name="Вакансия",
        related_name='interview_results'
    )
    
    qa_pairs = models.JSONField(
        verbose_name="Вопросы и ответы",
        encoder=DjangoJSONEncoder,
        default=list,
        help_text="Словарь вопросов и ответов в формате {'вопрос': 'ответ'}"
    )
    
    score_percentage = models.FloatField(
        verbose_name="Процент результата",
        default=0.0,
        help_text="Процент правильных/хороших ответов (0-100)"
    )
    
    assessment_text = models.TextField(
        verbose_name="Текстовая оценка",
        blank=True,
        null=True,
        help_text="Текстовая оценка от нейросети/HR"
    )
    
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Результат собеседования"
        verbose_name_plural = "Результаты собеседований"
        ordering = ['-created_at']
        unique_together = ['user', 'vacancy']  # Один результат на пользователя и вакансию

    def __str__(self):
        return f"Собеседование {self.user} на {self.vacancy} ({self.score_percentage}%)"
