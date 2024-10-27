from django.db import models
from hospital.models import Hospital
from django.conf import settings  

class CHP(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, null=True
    ) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    reg_no = models.CharField(max_length=255)
    location = models.TextField()
    sub_location = models.CharField(max_length=255)
    village = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.reg_no} - {self.user.username}"
