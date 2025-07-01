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
    
    # def get_absolute_url(self):
    #     return ('/employee/hr_profile/{self.id}')
    
    

# Create your models here.
