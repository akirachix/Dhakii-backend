from django.db import models
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField

class Careguide(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    image = models.URLField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255)
    content = HTMLField()
    author = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    
    def clean(self):
        if not self.title:
            raise ValidationError('Title cannot be empty.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
