from django.db import models
from django.conf import settings  # To refer to the User model


class CHP(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    ) 
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reg_no = models.CharField(max_length=255)
    location = models.TextField()
    sub_location = models.CharField(max_length=255)
    village = models.CharField(max_length=255)

    def __str__(self):
        
        return f"{self.reg_no} - {self.user.username}"  
