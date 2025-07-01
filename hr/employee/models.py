from django.db import models
from django.forms.widgets import TextInput

class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    conditions = models.TextField()
    interviews = models.IntegerField(default=0)
    isActive = models.BooleanField(default=False)
    
    def _str__(self):
        return self.title
    
# Create your models here.
