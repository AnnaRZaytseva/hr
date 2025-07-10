from django.db import models
from django.forms.widgets import TextInput
from django.contrib.auth import get_user_model

User = get_user_model()

class Vacancy(models.Model):
    title = models.CharField('Название',max_length=50)
    description = models.TextField('Описание')
    requirements = models.TextField('Требования')
    responsibilities = models.TextField('Обязанности')
    conditions = models.TextField('Условия')
    isActive = models.BooleanField('Отображается',default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-id']
        
        
from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
import json

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
        help_text="Процент правильных/хороших ответов (0-100)",
        # max_digits=5,
        # decimal_places=2
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
        # unique_together = ['user', 'vacancy']  # Один результат на пользователя и вакансию

    def __str__(self):
        return f"Собеседование {self.user} на {self.vacancy} ({self.score_percentage}%)"
    
    def save_qa_data(self, qa_dict):
        """Сохранение вопросов и ответов в JSON-формате"""
        self.qa_pairs = [{'question': q, 'answer': a} for q, a in qa_dict.items()]
        self.save()
    
    def calculate_score(self, passing_score=70):
        """Автоматический расчет процента (примерная реализация)"""
        total = len(self.qa_pairs)
        if total == 0:
            return 0
            
        good_answers = sum(1 for qa in self.qa_pairs if self._is_good_answer(qa['answer']))
        self.score_percentage = round((good_answers / total) * 100, 2)
        self.save()
        return self.score_percentage >= passing_score
    
    def _is_good_answer(self, answer):
        """Пример эвристики для оценки ответа (можно заменить на анализ нейросетью)"""
        return len(answer.split()) > 10  # Пример: ответ длиннее 10 слов