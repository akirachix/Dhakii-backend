from django.core.exceptions import ValidationError
from django.db import models

class Careguide(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True) 
    
    def clean(self):
    
        if not self.title:
            raise ValidationError('Title cannot be empty.')
        
    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title
