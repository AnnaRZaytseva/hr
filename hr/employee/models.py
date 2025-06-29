from django.db import models

class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    
    def _str__(self):
        return self.title
    
# Create your models here.
