from django.db import models

# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    
    def _str__(self):
        return self.title