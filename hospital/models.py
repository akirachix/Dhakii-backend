from django.db import models

# Create your models here.

class Hospital(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    type = models.CharField(max_length=255)  
    village = models.CharField(max_length=255)  
    hospital_location = models.CharField(max_length=255)  
    sub_location = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

   
    def __str__(self):
        return f"{self.name} {self.hospital_location}"
    
